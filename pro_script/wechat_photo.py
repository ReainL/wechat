#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 19-3-19
@title: '微信好友头像拼接'
@author: Xusl
"""
import itchat
import math
import PIL.Image as Image
import os

import logging.config

from config import logger_path

logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")


def photo_joint():
    func_name = "好友头像拼接"
    logger.info('start %s ' % func_name)
    itchat.auto_login(hotReload=True)
    itchat.dump_login_status()
    friends = itchat.get_friends(update=True)[0:]
    user = friends[0]["UserName"]

    num = 0
    pwd_path = os.path.abspath(os.path.dirname(os.getcwd()))
    desc_photos = os.path.join(pwd_path, 'res/photos')
    desc_full = os.path.join(pwd_path, 'res')

    for i in friends:
        img = itchat.get_head_img(userName=i["UserName"])
        file_image = open(desc_photos + "/" + str(num) + ".jpg", 'wb')
        file_image.write(img)
        file_image.close()
        num += 1

    ls = os.listdir(desc_photos)
    each_size = int(math.sqrt(float(640 * 640) / len(ls)))  # 算出每张图片的大小多少合适
    lines = int(640 / each_size)
    image = Image.new('RGBA', (640, 640))   # 创建640*640px的大图
    x = 0
    y = 0

    for i in range(0, len(ls) + 1):
        try:
            img = Image.open(desc_photos + "/" + str(i) + ".jpg")
        except IOError:
            print("Error")
        else:
            img = img.resize((each_size, each_size), Image.ANTIALIAS)
            image.paste(img, (x * each_size, y * each_size))    # 粘贴位置
            x += 1
            if x == lines:  # 换行
                x = 0
                y += 1

    image.save(desc_full + "/好友头像拼接图.jpg")
    itchat.send_image(desc_full + "/好友头像拼接图.jpg", 'filehelper')     # 拼接完成发送给文件传输助手
    logger.info('end %s ' % func_name)


def deal():
    """
    处理入口
    :return:
    """
    photo_joint()


if __name__ == '__main__':
    deal()
