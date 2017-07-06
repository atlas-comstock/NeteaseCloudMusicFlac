import re
import requests
import json
import urllib.request
import urllib.error
import os
import sys
test = False
test_url = r'http://music.163.com/#/playlist?id=88156914'
minimumsize = 10
if test:
    url = r'http://music.163.com/#/playlist?id=88156914'
else:
    print("fetching msg from %s \n" % sys.argv[1])
    url = re.sub("#/", "", sys.argv[1])
url = url.replace('/#/','/')
print(url)
r = requests.get(url)
contents = r.text
res = r'<ul class="f-hide">(.*?)</ul>'
mm = re.findall(res, contents, re.S | re.M)
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
if(mm):
    contents = mm[0]
else:
    print('Can not fetch information form URL. Please make sure the URL is right.\n')
    os._exit(0)
res = r'<textarea style="display:none;">(.*?)</textarea>'
mm = re.search(res, r.text, re.S | re.M).group(1)
try:
    results = json.loads(mm)
except:
    print('解析json失败')
not_found_list = []
for value in results:
    url = 'http://sug.music.baidu.com/info/suggestion'
    search_list = []
    search_list.append(value['name'])
    for artist in value['artists']:
        search_list.append(artist['name'])
    payload = {'word': '+'.join(search_list), 'version': '2', 'from': '0'}
    print('开始查找，查找关键词为:',payload)

    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if d is not None and 'data' not in d:
        print('未找到此歌曲信息')
        not_found_list.append(search_list[0])
        continue
    songid = d["data"]["song"][0]["songid"]
    print("find songid: %s" % songid)

    url = "http://music.baidu.com/data/music/fmlink"
    payload = {'songIds': songid, 'type': 'flac'}
    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if('data' not in d) or d['data'] == '':
        continue
    songlink = d["data"]["songList"][0]["songLink"]
    print("find songlink: ")
    if(len(songlink) < 10):
        print("\tdo not have flac\n")
        not_found_list.append(search_list[0])
        continue
    print(songlink)

    songdir = "songs_dir"
    if not os.path.exists(songdir):
        os.makedirs(songdir)

    songname = d["data"]["songList"][0]["songName"]
    artistName = d["data"]["songList"][0]["artistName"]
    filename = ("%s/%s/%s-%s.flac" %
                (CURRENT_PATH, songdir, songname, artistName))

    f = urllib.request.urlopen(songlink)
    headers = requests.head(songlink).headers
    size = round(int(headers['Content-Length']) / (1024 ** 2), 2)
    #Download unfinished Flacs again.
    if not os.path.isfile(filename) or os.path.getsize(filename) < minimumsize: #Delete useless flacs
        print("%s is downloading now ......\n\n" % songname)
        if size >= minimumsize:
            with open(filename, "wb") as code:
                code.write(f.read())
        else:
            print("the size of %s (%r Mb) is less than 10 Mb, skipping" %
                  (filename, size))
            not_found_list.append(search_list[0])
    else:
        print("%s is already downloaded. Finding next song...\n\n" % songname)


print("\n================================================================\n")
print("Download finish!\nSongs' directory is %s/songs_dir" % os.getcwd())
print('未下载的歌曲如下\n')
print(' '.join(not_found_list))
