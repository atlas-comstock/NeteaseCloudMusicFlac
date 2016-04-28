import re
import requests
#import json
#import urllib2
#import os
url = 'http://music.163.com/playlist?id=39123016'
r = requests.get(url)
contents = r.text
#print contents
#print 'getcontent'
res = r'<ul class="f-hide">(.*?)</ul>'
mm =  re.findall(res, contents, re.S|re.M)
#print mm[0]
#print 'getcontent'
contents = mm[0]
res = r'<li><a .*?>(.*?)</a></li>'
mm =  re.findall(res, contents, re.S|re.M)
for value in mm:
    print value

#url = 'http://sug.music.baidu.com/info/suggestion'
#payload = {'word': 'wo', 'version': '2', 'from': '0'}
#
#r = requests.get(url, params=payload)
#contents = r.text
#d = json.loads(contents, encoding="utf-8")
#songid = d["data"]["song"][0]["songid"]
#print songid
#
#url = "http://music.baidu.com/data/music/fmlink"
#payload = {'songIds': songid, 'type': 'flac'}
#r = requests.get(url, params=payload)
##print r.text
#contents = r.text
#d = json.loads(contents, encoding="utf-8")
##print d
##print json_str
#songlink = d["data"]["songList"][0]["songLink"]
#print songlink
#
#songdir = "songs_dir"
#if not os.path.exists(songdir):
#    os.makedirs(songdir)
#
#songname = d["data"]["songList"][0]["songName"]
#artistName = d["data"]["songList"][0]["artistName"]
#filename = "./" + songdir + "/"+songname+"-"+artistName+".flac"
#print filename
#
#
#f = urllib2.urlopen(songlink)
#with open(filename, "wb") as code:
#   code.write(f.read())
#
## POST with form-encoded data
#r = requests.post(url, data=payload)
#print r.text
#
## POST with JSON
#import json
#r = requests.post(url, data=json.dumps(payload))
#print r.text
#
## Response, status etc
#r.text
#r.status_code
