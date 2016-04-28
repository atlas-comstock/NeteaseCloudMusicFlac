import requests
import json
import urllib2
import os
url = 'http://sug.music.baidu.com/info/suggestion'
payload = {'word': 'wo', 'version': '2', 'from': '0'}

# GET
#r = requests.get(url)
#print r.text
#x = r.text

# GET with params in URL
r = requests.get(url, params=payload)
#print r.text
contents = r.text
d = json.loads(contents, encoding="utf-8")
#print d
#json_str = json.dumps(d, ensure_ascii=False,indent=4)
#print json_str
#print d["data"]["song"][0]["songid"]
songid = d["data"]["song"][0]["songid"]
print songid

url = "http://music.baidu.com/data/music/fmlink"
payload = {'songIds': songid, 'type': 'flac'}
r = requests.get(url, params=payload)
#print r.text
contents = r.text
d = json.loads(contents, encoding="utf-8")
#print d
#json_str = json.dumps(d, ensure_ascii=False,indent=4)
#print json_str
songlink = d["data"]["songList"][0]["songLink"]
print songlink

songdir = "songs_dir"
if not os.path.exists(songdir):
    os.makedirs(songdir)

songname = d["data"]["songList"][0]["songName"]
artistName = d["data"]["songList"][0]["artistName"]
filename = "./" + songdir + "/"+songname+"-"+artistName+".flac"
print filename


f = urllib2.urlopen(songlink)
with open(filename, "wb") as code:
   code.write(f.read())
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
