# NeteaseCloudMusicFlac

#### [感谢](https://github.com/imfangli/baidu-music-downloader)为 NeteaseCloudMusicFlac 的开发付出过努力以及提出建议的每一个人！


根据网易云音乐歌单, 下载对应无损FLAC歌曲到本地.

### 安装

#### 安装Python
[根据此网站教程安装Python](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001374738150500472fd5785c194ebea336061163a8a974000)

#### 下载main.py
下载此网站上的main.py

### 获取歌单
到[网易云音乐网页版](http://music.163.com/#)找出想要下载无损的歌单, 如下图

![NeteaseCloudMusicFlac](http://av.jejeso.com/pic.png)

后进入歌单, 地址栏地址便是歌单地址.
但是要把http://music.163.com/#/playlist?id=145258012里的#/删除掉

### 使用

	$ python main.py 歌单地址(如上图便是: http://music.163.com/playlist?id=145258012)

### 示例命令

	$ python main.py http://music.163.com/playlist?id=145258012

### 如果告知缺乏module
下载对应的模块(module), 网上搜索如何安装python模块.

	pip install requests

### TODO list
1. 使用PEP8 Python 编码规范整理代码
2. 目前只是匹配歌曲名字, 最好加上匹配歌手名
3. 歌曲匹配率不高, 可以考虑再到其他网站抓

Enjoy it !
如侵权, 请告知, 马上停止该项目.


### The MIT License (MIT)

CopyRight (c) 2015 YongHaoHu  &lt;<a href="christopherwuy@gmail.com">christopherwuy@gmail.com</a>&gt;

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
