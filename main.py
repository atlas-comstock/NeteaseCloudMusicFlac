import re
import requests
import json
import urllib2
import os
import sys

print "fetching msg from " + sys.argv[1] + "\n"
url = re.sub("#/", "", sys.argv[1])
r   = requests.get(url)
contents = r.text
res = r'<ul class="f-hide">(.*?)</ul>'
mm  =  re.findall(res, contents, re.S|re.M)
if(mm):
    contents = mm[0]
else:
    print 'Can not fetch information form URL. Please make sure the URL is right.\n'
    os._exit(0)

res = r'<li><a .*?>(.*?)</a></li>'
mm  =  re.findall(res, contents, re.S|re.M)

for value in mm:
    url = 'http://sug.music.baidu.com/info/suggestion'
    payload = {'word': value, 'version': '2', 'from': '0'}
    print value

    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if('data' not in d):
        continue
    songid = d["data"]["song"][0]["songid"]
    print "find songid: "
    print songid

    url = "http://music.baidu.com/data/music/fmlink"
    payload = {'songIds': songid, 'type': 'flac'}
    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if('data' not in d):
        continue
    songlink = d["data"]["songList"][0]["songLink"]
    print "find songlink: "
    if(len(songlink) < 10):
        print "\tdo not have flac\n"
        continue
    print songlink

    songdir = "songs_dir"
    if not os.path.exists(songdir):
        os.makedirs(songdir)

    songname = d["data"]["songList"][0]["songName"]
    artistName = d["data"]["songList"][0]["artistName"]
    filename = "./" + songdir + "/"+songname+"-"+artistName+".flac"
    print filename + " is downloading now ......\n\n"

    f = urllib2.urlopen(songlink)
    with open(filename, "wb") as code:
        code.write(f.read())
    
    if os.path.getsize(filename) < 10000 * 1024: #Source from http://stackoverflow.com/questions/8626325/most-efficient-way-to-delete-a-file-if-its-below-a-certain-size
        os.remove(filename)
        print "\nFile removed as it is under 10 Mb."
print "\n================================================================"
print "\nDownload finish!\nSongs' directory is " + os.getcwd() + "/songs_dir"
