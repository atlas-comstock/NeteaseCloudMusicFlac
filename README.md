# NeteaseCloudMusicFlac

#### [感谢](https://github.com/imfangli/baidu-music-downloader)为 NeteaseCloudMusicFlac 的开发付出过努力以及提出建议的每一个人！

* [Elixir 实现](https://github.com/YongHaoWu/NeteaseCloudMusicFlacElixir)
* [golang 实现](https://github.com/lifei6671/NeteaseCloudMusicFlac)

根据网易云音乐歌单, 下载对应无损FLAC歌曲到本地.

### BackGround
现在无损资源基本都是专辑, 很难找到单曲来下载.
而且下载需要每个专辑搜索一遍, 需要用云盘复制粘贴密码再下载.
这对于听Hi-Fi的人们来说是非常不便利的事情, 找歌曲可以找一整天.
而现在网易云音乐是绝大多数人听在线歌曲的平台, 歌单众多.
于是我想做如此一个项目, 根据网易云音乐上面的歌单, 自动下载FLAC无损音乐到本地.

### 注意
海外由于版权问题无法下载歌曲, 所以会导致此[issue](https://github.com/YongHaoWu/NeteaseCloudMusicFlac/issues/1), 无法正常使用, 需要修改DNS配置, 里面有解决方法.

### 安装

#### 安装Python
[根据此网站教程安装Python](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001374738150500472fd5785c194ebea336061163a8a974000)

#### 下载main.py或者python3_main.py

python2下载使用此网站上的main.py

python3下载使用此网站上的python3_main.py

### 获取歌单
到[网易云音乐网页版](http://music.163.com/#)找出想要下载无损的歌单, 如下图

![NeteaseCloudMusicFlac](http://av.jejeso.com/pic.png)

后进入歌单, 地址栏地址便是歌单地址.

### 使用

	$ python main.py 歌单地址(如上图便是: http://music.163.com/#/playlist?id=145258012)

### python2示例命令

	$ python main.py 'http://music.163.com/#/playlist?id=145258012'

### python3示例命令

	$ python3 python3_main.py 'http://music.163.com/#/playlist?id=145258012'


### 如果告知缺乏module
下载对应的模块(module), 网上搜索如何安装python模块.

###### python2
	pip install requests

##### python3
	pip3 install requests

### TODO list
1. 目前只是匹配歌曲名字, 最好加上匹配歌手名
2. 歌曲匹配率不高, 可以考虑再到其他网站抓

Enjoy it !

### 版权问题
如果涉及版权问题，项目将立刻关闭。
自己为百度音乐会员, 该项目为方便自己而做


### The MIT License (MIT)

CopyRight (c) 2016 YongHaoHu  &lt;<a href="christopherwuy@gmail.com">christopherwuy@gmail.com</a>&gt;

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
