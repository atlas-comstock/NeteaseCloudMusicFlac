import re
import requests
import json
import urllib2
import os, sys

print "fetching msg from "+sys.argv[1]+"\n Please make sure the url is right.\n"
url = sys.argv[1]
#url = 'http://music.163.com/playlist?id=39123016'
r = requests.get(url)
contents = r.text
#print contents
#print 'getcontent'
res = r'<ul class="f-hide">(.*?)</ul>'
mm =  re.findall(res, contents, re.S|re.M)
#print mm
#print 'getcontent'
if(mm):
    contents = mm[0]
else:
    os._exit()

res = r'<li><a .*?>(.*?)</a></li>'
mm =  re.findall(res, contents, re.S|re.M)
#i = 0
for value in mm:
#    if i > 10:
#        break
#    i = i+1
    url = 'http://sug.music.baidu.com/info/suggestion'
    payload = {'word': value, 'version': '2', 'from': '0'}
    print value

    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if(d.has_key('data')!=True ):#or d.has_key('song')!=True or d.has_key('songid')!=True
        continue
    songid = d["data"]["song"][0]["songid"]
    print "find songid: "
    print songid

    url = "http://music.baidu.com/data/music/fmlink"
    payload = {'songIds': songid, 'type': 'flac'}
    r = requests.get(url, params=payload)
    #print r.text
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    #print d
    #print json_str
    if(d.has_key('data')!=True | d.has_key('songList')!=True | d.has_key('songLink')!=True):
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
