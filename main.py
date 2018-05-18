# -*- coding: utf-8 -*-
import re
import requests
import json
import urllib2
import os
import sys

def fetch_song_list(url):
    header_value = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36\
            (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}
    r = requests.get(url, headers=header_value)
    contents = r.text
    res = r'<ul class="f-hide">(.*?)</ul>'
    song_list = re.findall(res, contents, re.S | re.M)
    if(song_list):
        contents = song_list[0]
    else:
        print 'Can not fetch information form URL. Please make sure the URL is right.\n'
        os._exit(0)

    res = r'<li><a .*?>(.*?)</a></li>'
    song_names = re.findall(res, contents, re.S | re.M)
    return song_names

def ensure_download_dir_exist():
    songdir = "songs_dir"
    if not os.path.exists(songdir):
        os.makedirs(songdir)
    return songdir

def get_songid(value):
    value = value.replace('\\xa0', ' ')# windows cmd 的编码问题
    print value
    url = 'http://sug.music.baidu.com/info/suggestion'
    payload = {'word': value, 'version': '2', 'from': '0'}

    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if('data' not in d):
        return ""
    songid = d["data"]["song"][0]["songid"]
    print "songid: " + songid
    return songid

def get_song_info(songid):
    url = "http://music.baidu.com/data/music/fmlink"
    payload = {'songIds': songid, 'type': 'flac'}
    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    return d

def extract_song_info(key):
    name = d["data"]["songList"][0][key]
    name = "".join(name.split())
    for c in r'[\\/:*?\"<>|]':
        name = name.replace(c,'')
    return name



minimumsize = 10
songdir = ensure_download_dir_exist()

url = re.sub("#/", "", sys.argv[1]).strip()
print "fetching Netease song list from " + url + "\n"
song_names = fetch_song_list(url)
for value in song_names:
    songid = get_songid(value)
    if songid == "":
        continue

    d = get_song_info(songid)
    if d is not None and 'data' not in d or d['data'] == '' or d['data']["songList"] == '':
        continue

    songlink = d["data"]["songList"][0]["songLink"]
    if(len(songlink) < 10):
        print "\tdo not have flac\n"
        continue
    print "songlink: " + songlink

    songName = extract_song_info("songName")
    songName = songName.replace('/', "%2F").replace('\"', "%22")

    artistName = extract_song_info("artistName")

    filename = "./" + songdir + "/" + songName + "-" + artistName + ".flac"

    f = urllib2.urlopen(songlink)

    headers = requests.head(songlink).headers
    if 'Content-Length' in headers:
        size = round(int(headers['Content-Length']) / (1024 ** 2), 2)
    else:
        print "\tdo not have Content-Length header\n"
        continue
    #Download unfinished Flacs again.
    if not os.path.isfile(filename) or os.path.getsize(filename) < minimumsize:
        print "%s is downloading to path %s now ......\n" %(songName, filename)
        if size >= minimumsize:
            with open(filename, "wb") as code:
                code.write(f.read())
            print "Download %s is finished.\n" % songName
        else:
            print "the size of %s (%r Mb) is less than 10 Mb, skipping\n\n" % (filename, size)
    else:
        print "%s is already downloaded. Finding next song...\n\n" % songName

print "\n================================================================\n"
print "Download finish!\nSongs' directory is " + os.getcwd() + "/songs_dir"
