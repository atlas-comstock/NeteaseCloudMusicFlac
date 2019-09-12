#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections
import re
import logging
import argparse
import requests
import json
import os
import sys
import unicodedata
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import tqdm

MINIMUM_SIZE = 10
DOWNLOAD_DIR = os.path.join(os.getcwd(), "songs_dir")
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
LOG_LEVEL = logging.INFO
LOG_FILE = 'download.log' or False
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
}


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
        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
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

    logger.info("歌单: " + song_list_name + "\n")
    pattern = r'<li><a href="/song\?id=\d+">(.+?)</a></li>'
    song_list = re.findall(pattern, contents)
    if not song_list:
        logger.error(
            '不能解析歌单 url\n')
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
    BAIDU_SUGGESTION_API = 'http://musicapi.qianqian.com/v1/restserver/ting'
    payload = {
        "query": value,
        "method": "baidu.ting.search.common",
        "format": "json",
        "page_no": 1,
        "page_size": 5,
    }
    # value = value.replace('\\xa0', ' ')  # windows cmd 的编码问题

    r = requests.get(BAIDU_SUGGESTION_API, params=payload, headers=HEADERS)
    try:
        contents = r.json()
        songid = contents['song_list'][0]['song_id']
    except:
        logger.info("未查找到歌曲 %s 对应的ID" % value)
        songid = ""
    finally:
        return songid
    # if r.status_code != 200 or r.headers.get("Content-Type") != 'application/json':


def get_song_info(songid):
    BAIDU_MUSIC_API = "http://music.baidu.com/data/music/fmlink"
    payload = {'songIds': songid, 'type': 'flac'}
    r = requests.get(BAIDU_MUSIC_API, params=payload, headers=HEADERS)
    contents = json.loads(r.text)
    song_info = {}
    if (contents['errorCode'] == 22000):
        song_info['songname'] = contents['data']['songList'][0]['songName']
        song_info['artist'] = contents['data']['songList'][0]['artistName']
        song_info['link'] = contents['data']['songList'][0]['songLink'] or None
        size = contents['data']['songList'][0]['size']

        if song_info['link'] and size:
            song_info['size'] = round(int(size) / (1024 ** 2))
            song_info['data'] = True
        else:
            song_info['data'] = False

    else:
        song_info['data'] = False

    logger.info("获取歌曲信息 %s" % json.dumps(song_info))
    return song_info


def download_song(song_info, session, mp3_option, download_folder, display, counter):
    if (song_info['data']):
        if not mp3_option and song_info['size'] < 10:
            logger.info("%s-%s 文件大小小于 10MB, 放弃下载。" %
                        (song_info['songname'], song_info['artist']))
            counter['giveup'] += 1
            display.update()
            return None
        else:
            filename = "{0}-{1}.flac".format(
                validate_file_name(song_info['songname']),
                validate_file_name(song_info['artist']))

            filepath = os.path.join(download_folder, filename)
            logger.info("下载中: %s" % filepath)
            try:
                r = session.get(song_info['link'], headers=HEADERS, timeout=3)
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                logger.info("下载完成: %s " % filepath)

                counter["success"] += 1
                display.update()
            except requests.exceptions.Timeout as err:
                logger.error("%s during download filepath" % err)
                counter['error'] += 1
                display.update()


def main():
    start = time.time()

    if not os.path.exists(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)

    url, mp3_option = get_args()
    if mp3_option:
        logger.info("将下载所有歌曲, 包括 MP3 格式.")
    song_list_name, song_list = fetch_song_list(url)
    logger.info("歌单中包含的歌曲有: %s" % song_list)

    download_folder = os.path.join(DOWNLOAD_DIR, validate_file_name(song_list_name))
    if not os.path.exists(download_folder):
        os.mkdir(download_folder)

    with ThreadPoolExecutor(max_workers=10) as executor:
        counter = collections.Counter()
        song_ids = executor.map(get_songid, song_list)
        song_infos = executor.map(get_song_info, song_ids)
        res = [i for i in song_infos if i['data'] == True]
        logger.info("获取歌曲信息完成，开始下载。")
        session = requests.session()
        d = tqdm.tqdm(total=len(res))
        download = partial(download_song, session=session, mp3_option=mp3_option,
                           download_folder=download_folder, display=d, counter=counter)
        executor.map(download, res)

    end = time.time()
    logger.info("共耗时 %s s", str(end - start))
    logger.info("共完成{}首歌曲的搜索，成功下载歌曲{}首，资源不满足要求未下载的歌曲数为：{}首, 下载失败的歌曲数为："
                "{}首，未找到下载资源的歌曲数为：{}首"
          .format(len(song_list), counter['success'], counter['giveup'], counter['error'], len(song_list) - len(res)))


# 禁止 requests 模组使用系统代理
os.environ['no_proxy'] = '*'
logger = set_logger()

if __name__ == "__main__":
    main()
