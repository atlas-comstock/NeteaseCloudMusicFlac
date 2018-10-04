#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import logging
import requests
import json
import urllib.request
import urllib.error
import os
import sys
import unicodedata
import time
from multiprocessing.dummy import Pool

MINIMUM_SIZE = 10
DOWNLOAD_DIR = "songs_dir"
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
LOG_LEVEL = logging.INFO
LOG_FILE = 'download.log' or False
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s'
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

logger = set_logger()

def fetch_song_list(url):
    logger.info("fetching Netease song list from " + url + "\n")
    r = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'})
    contents = r.text
    res = r'<ul class="f-hide">(.*?)</ul>'
    mm = re.findall(res, contents, re.S | re.M)
    if (mm):
        contents = mm[0]
    else:
        logger.error('Can not fetch information form URL. Please make sure the URL is right.\n')
        os._exit(0)

    res = r'<li><a .*?>(.*?)</a></li>'
    song_names = re.findall(res, contents, re.S | re.M)
    return song_names

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

   r = requests.get(BAIDU_SUGGESTION_API, params=payload)
   contents = r.text
   d = json.loads(contents, encoding="utf-8")
   if d is not None and 'data' not in d:
       return ""
   else:
       songid = d["data"]["song"][0]["songid"]
       logger.info("find songid: %s" % songid)
       return songid

def get_song_info(songid):
    BAIDU_MUSIC_API = "http://music.baidu.com/data/music/fmlink"
    payload = {'songIds': songid, 'type': 'flac'}
    r = requests.get(BAIDU_MUSIC_API, params=payload)
    contents = r.text
    return json.loads(contents, encoding="utf-8")

def download_song(d, songlink, is_skip_mp3_songs):
   songname = d["data"]["songList"][0]["songName"]
   songname = validate_file_name(songname)
   artistName = d["data"]["songList"][0]["artistName"]
   artistName = validate_file_name(artistName)

   filename = ("%s/%s/%s-%s.flac" %
               (CURRENT_PATH, DOWNLOAD_DIR, songname, artistName))

   f = urllib.request.urlopen(songlink, timeout=10)
   headers = requests.head(songlink).headers
   if 'Content-Length' in headers:
       size = round(int(headers['Content-Length']) / (1024 ** 2), 2)
   else:
       return

   # Download unfinished Flacs again.
   # Delete useless flacs
   if not os.path.isfile(filename) or (is_skip_mp3_songs and os.path.getsize(filename) < MINIMUM_SIZE):
       logger.info("%s is downloading now ......\n\n" % songname)
       if (not is_skip_mp3_songs) or size >= MINIMUM_SIZE:
           with open(filename, "wb") as code:
               code.write(f.read())
           logger.info("%s finished downloading ......\n\n" % songname)
       else:
           logger.warning("the size of %s (%r Mb) is less than 10 Mb, skipping" %
                 (filename, size))
   else:
       logger.info("%s is already downloaded. Finding next song...\n\n" % songname)

def main():
    if len(sys.argv) < 2:
         print("请在 python3 后加上 你要下载的网易云音乐的歌单的 url\n")
         print("示例: python3 main.py 'http://music.163.com/#/playlist?id=145258012'\n")
         exit()
    is_skip_mp3_songs = True
    if len(sys.argv) > 2:
         print("将下载所有歌曲, 包括 MP3 格式 \n")
         is_skip_mp3_songs= False
    url = re.sub("#/", "", sys.argv[1]).strip()
    song_names = fetch_song_list(url)
    p = Pool()
    for value in song_names:
        songid = get_songid(value)
        if songid == "":
            continue

        d = get_song_info(songid)
        if ('data' not in d) or d['data'] == '' or d['data']['songList'] == '':
            continue

        songlink = d["data"]["songList"][0]["songLink"]
        logger.info("find songlink: ")
        if (len(songlink) < 10):
            logger.warning("\tdo not have flac\n")
            continue
        logger.info(songlink)

        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        # download_song(d, songlink)
        p.apply_async(download_song, args=(d, songlink, is_skip_mp3_songs))
    logger.info("\n================================================================\n")
    logger.info('Waiting for all download subprocesses done...')
    p.close()
    p.join()

    logger.info("\n================================================================\n")
    logger.info("Download finish!\nSongs' directory is %s/songs_dir" % os.getcwd())

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    logger.info("cost %s s", str(end - start))
