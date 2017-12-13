# get_data.py:
# A Function that acquire CAPTCHA data from PKU Dean website
# By He Hao, 1600012742@pku.edu.cn

import urllib2
import time
import os


# get_data: Get random CAPTCHA images from PKU Dean website automatically
# Parameters: num - Number of images to acquire
#             folder - The folder to store these images
def get_data(num, folder):
    cnt = 1
    if not os.path.exists(folder):
        os.makedirs(folder)
    while cnt <= num:
        time.sleep(1)
        im_url = 'http://dean.pku.edu.cn/student/yanzheng.php?act=init'
        im_data = urllib2.urlopen(im_url).read()
        f = open(folder + os.sep + str(cnt) + '.png', 'wb')
        f.write(im_data)
        f.close()
        cnt += 1

