#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import logging
import argparse
import requests
import json
import urllib.request
import urllib.error
import os
import sys
import unicodedata
import time
from multiprocessing.dummy import Pool
from functools import partial

MINIMUM_SIZE = 10
DOWNLOAD_DIR = os.path.join(os.getcwd(), "songs_dir")
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
LOG_LEVEL = logging.INFO
LOG_FILE = 'download.log' or False
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
}


def init():
    if not os.path.exists(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)


def get_args():
    parser = argparse.ArgumentParser(
        usage="python main.py 歌单地址",
        description="根据网易云音乐歌单, 下载对应无损FLAC歌曲到本地."
    )
    parser.add_argument('playlist_url', type=str, help="网易云音乐歌单url")
    parser.add_argument('-m', '--mp3', action="store_true",
                        dest='mp3_option', help="下载mp3资源")
    parse_result = parser.parse_args()
    url = parse_result.playlist_url
    mp3_option = parse_result.mp3_option

    return url, mp3_option


def set_logger():
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if LOG_FILE:
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(LOG_LEVEL)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def fetch_song_list(url):
    _id = re.search(r'id=(\d+)', url).group(1)
    url = "http://music.163.com/playlist?id={0}".format(_id)
    r = requests.get(url, headers=HEADERS)
    contents = r.text
    song_list_name = re.search(r"<title>(.+)</title>", contents).group(1)[:-13]

    logger.info("fetching Netease song list from " + song_list_name + "\n")
    pattern = r'<li><a href="/song\?id=\d+">(.+?)</a></li>'
    song_list = re.findall(pattern, contents)
    if not song_list:
        logger.error(
            'Can not fetch information form URL. Please make sure the URL is right.\n')
        sys.exit(1)

    return song_list_name, song_list


def validate_file_name(songname):
    # trans chinese punctuation to english
    songname = unicodedata.normalize('NFKC', songname)
    songname = songname.replace('/', "%2F").replace('\"', "%22")
    rstr = r"[\/\\\:\*\?\"\<\>\|\+\-:;',=.?@]"
    # Replace the reserved characters in the song name to '-'
    rstr = r"[\/\\\:\*\?\"\<\>\|\+\-:;=?@]"  # '/ \ : * ? " < > |'
    return re.sub(rstr, "_", songname)


def get_songid(value):
    BAIDU_SUGGESTION_API = 'http://sug.music.baidu.com/info/suggestion'
    payload = {'word': value, 'version': '2', 'from': '0'}
    value = value.replace('\\xa0', ' ')  # windows cmd 的编码问题
    logger.info(value)

    r = requests.get(BAIDU_SUGGESTION_API, params=payload, headers=HEADERS)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if not d or "errno" in d:
        return ""
    else:
        songid = d["data"]["song"][0]["songid"]
        logger.info("Find songid: %s" % songid)
    return songid


def get_song_info(songid):
    BAIDU_MUSIC_API = "http://music.baidu.com/data/music/fmlink"
    payload = {'songIds': songid, 'type': 'flac'}
    r = requests.get(BAIDU_MUSIC_API, params=payload, headers=HEADERS)
    contents = json.loads(r.text)
    song_info = {}
    if(contents['errorCode'] == 22000):
        song_info['songname'] = contents['data']['songList'][0]['songName']
        song_info['artist'] = contents['data']['songList'][0]['artistName']

        link = contents['data']['songList'][0]['songLink']
        song_info['link'] = link or None
        size = contents['data']['songList'][0]['size']
        if(size):
            song_info['size'] = round(int(size) / (1024 ** 2))
        else:
            song_info['size'] = None

        if(song_info['link'] and song_info['size']):
            song_info['data'] = True
        else:
            song_info['data'] = False
    else:
        song_info['data'] = False

    logger.info("Get song info %s" % json.dumps(song_info))
    return song_info


def download_song(song_info, mp3_option, download_folder):
    if(song_info['data']):
        if not mp3_option and song_info['size'] < 10:
            return None
        else:
            filename = "{0}-{1}.flac".format(
                validate_file_name(song_info['songname']),
                validate_file_name(song_info['artist']))

            filepath = os.path.join(download_folder, filename)
            r = requests.get(song_info['link'], headers=HEADERS, timeout=4)
            logger.info("Downloading : %s" % filepath)
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            logger.info("%s downloaded" % filepath)


def main():
    start = time.time()

    init()
    url, mp3_option = get_args()
    if mp3_option:
        logger.info("将下载所有歌曲, 包括 MP3 格式.")
    song_list_name, song_list = fetch_song_list(url)

    pool = Pool()
    song_ids = pool.map(get_songid, song_list)
    song_infos = pool.map(get_song_info, song_ids)

    download_folder = os.path.join(DOWNLOAD_DIR, song_list_name)
    if not os.path.exists(download_folder):
        os.mkdir(download_folder)

    logger.info("Start Downloading")
    download = partial(download_song, mp3_option=mp3_option,
                       download_folder=download_folder)
    
    for i in range(1, len(song_infos), 4):
        pool.map(download, song_infos[i-1:i+4-1])
        time.sleep(1)

    pool.close()
    pool.join()
    end = time.time()
    logger.info("cost %s s", str(end - start))


os.environ['no_proxy'] = '*'
logger = set_logger()

if __name__ == "__main__":
    main()
