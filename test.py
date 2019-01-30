import shutil, tempfile
import logging
import unittest
import json
import re
import os
import time
from main import set_logger, fetch_song_list, get_songid, get_song_info, download_song
from main import MINIMUM_SIZE


class Test(unittest.TestCase):

    # def setUp(self):
    #     self.test_dir = tempfile.mkdtemp()  
    #     print(self.test_dir)
    # def tearDown(self):
    #     shutil.rmtree(self.test_dir)
    def test_fetch_song_list(self):
        correct_url = "https://music.163.com/#/playlist?id=2594603185"
        correct_url_songlist = [
            'Careless Whisper',
            'Be Free',
            'How Long Will I Love You',
            'Wham Bam Shang-A-Lang',
            'California Dreaming (重庆森林)',
            'Talk Baby Talk',
            '水边的阿狄丽娜',
            'Levels',
            'Ode an die Freude',
            'Let Me Know'
            ]
        wrong_url = "id=22"

        self.assertEqual(len(fetch_song_list(correct_url)[1]) , 10)
        self.assertCountEqual(fetch_song_list(correct_url)[1], correct_url_songlist)
        with self.assertRaises(SystemExit) as cm:
            fetch_song_list(wrong_url)
        self.assertEqual(cm.exception.code, 1)
    def test_get_songid(self):
        correct_name = "Let Me Know"
        _id = '2043287'

        wrong_name = "youmeiyouzheyangyishouge"
        
        
        self.assertEqual(get_songid(correct_name), _id)
        self.assertEqual(get_songid(wrong_name), "")

    def test_get_song_info(self):
        correct_id = '296532523'
        correct_song_info = {
            'songname': "Careless Whisper",
            'artist': "Sharon Cuneta,Andrew Ridgeley,George Michael",
            'link': "http://zhangmenshiting.qianqian.com/data2/music/14a5cc3a8be3f13184e155c69e59d4b7/594663375/\\d+.flac\\?xcode=.+",
            'size': 39,
            'data': True
        }

        wrong_id = ['2', '2233']
        wrong_song_info = {
            'data': False
        }
        song_info = get_song_info(correct_id)
        self.assertRegex(song_info['link'], correct_song_info['link'])

        del song_info['link']
        del correct_song_info['link']

        self.assertEqual(song_info, correct_song_info)
        for _id in wrong_id:
            self.assertEqual(get_song_info(_id), wrong_song_info)

    # def test_download_song(self):
    #     songlist = fetch_song_list('https://music.163.com/#/playlist?id=2616291276')
    #     song_ids = map(get_songid, songlist)
    #     data = list(map(get_song_info, song_ids))

    #     count_flac = 0
    #     for i in range(len(data)):
    #         if data[i]['size'] >= MINIMUM_SIZE:
    #             count_flac += 1

    #     def lam(mp3_option):
    #         for n in data:
    #             download_song(n, mp3_option, self.test_dir)
    #             time.sleep(1)
 
    #         count = 0

    #         files = os.listdir(self.test_dir)
    #         if not mp3_option:
    #             for file in files:
    #                 file_size = os.path.getsize(os.path.join(self.test_dir, file))/(1024 ** 2)
    #                 print("filesize:{}".format(file_size))
    #                 if file_size >= MINIMUM_SIZE:
    #                     count += 1
    #             self.assertEqual(count, count_flac)
    #         else:
    #             self.assertEqual(len(files), len(data))

    #     lam(False)
    #     shutil.rmtree(self.test_dir)
    #     self.test_dir = tempfile.mkdtemp()
    #     lam(True)
        



if __name__ == '__main__':
    unittest.main()

