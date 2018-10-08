# -*- coding: utf-8 -*-
import requests
import base64
result = requests.get("http://apps04.cnpc/MPG/spxw/“一带一路”上有我.wmv").content
with open('my_video.mp4', 'wb') as f:
    f.write(result)
# base64_data = base64.b64encode(result.content)
# print base64_data
# u = u"“一带一路”上有我"
# print u
# mplayer mms://EIPCNPCWEB01.cnpc.com.cn/Hq_Vedio/spxw/“一带一路”上有我.wmv -dumpstream -dumpfile a.wmv
# import os
# # os.system("D:\MPlayer-x86_64-r38116+gf4cf6ba8c9\mplayer.exe mms://EIPCNPCWEB01.cnpc.com.cn/Hq_Vedio/spxw/\xa1\xb0\xd2\xbb\xb4\xf8\xd2\xbb\xc2\xb7\xa1\xb1\xc9\xcf\xd3\xd0\xce\xd2.wmv")
# os.system("D:\MPlayer-x86_64-r38116+gf4cf6ba8c9\mplayer.exe mms://EIPCNPCWEB01.cnpc.com.cn/Hq_Vedio/spxw/“一带一路”上有我.wmv")
#
# 'http://apps04.cnpc/MPG/spxw/“一带一路”上有我.wmv'
# '//*[@id="MediaPlayer"]/param[2]'