#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 19-3-20
@title: '微信好友个性签名词云图展示'
@author: Xusl
"""
import os
import logging.config
import matplotlib.pyplot as plt
import jieba
import re
import numpy as np

from config import logger_path
from pro_script.wechat_login import wc_login
from scipy.misc import imread
from snownlp import SnowNLP
from wordcloud import WordCloud, ImageColorGenerator


logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")

pwd_path = os.path.abspath(os.path.dirname(os.getcwd()))
res_full = os.path.join(pwd_path, 'res/')


def sign_words(fri_infos):
    """
    好友个性签名
    :param fri_infos:
    :return:
    """
    func_name = "好友个性签名"
    logger.info('start %s ' % func_name)
    sign_li = []
    rule = re.compile("1f\d+\w*|[<>/=]")    # 定义正则规则
    for fri_info in fri_infos:
        signature = fri_info['signature']
        if signature:
            sign_deal = signature.replace('\n', '').replace('\t', '').replace(' ', '')\
                .replace("span", "").replace("class", "").replace("emoji", "")
            sign = rule.sub("", sign_deal)
            sign_li.append(sign)

    logger.debug('sign_li: %s' % sign_li)
    logger.info('end %s ' % func_name)
    return sign_li


def word_cloud(comment):
    """
    词云图
    :param comment:
    :return:
    """
    func_name = "词云图"
    logger.info('start %s ' % func_name)
    conf_path = os.path.join(pwd_path, 'conf/')
    comment_txt = ''
    back_img = plt.imread(conf_path + '/peiqi.jpg')
    cloud = WordCloud(font_path=conf_path + '/simhei.ttf',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
                      background_color="white",  # 背景颜色
                      max_words=5000,  # 词云显示的最大词数
                      mask=back_img,  # 设置背景图片
                      max_font_size=100,  # 字体最大值
                      random_state=42,
                      width=360, height=591, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,保存的图片大小将会按照其大小保存,margin为词语边缘距离
                      )
    for li in comment:
        comment_txt += ' '.join(jieba.cut(li, cut_all=False))
    wc = cloud.generate(comment_txt)
    image_colors = ImageColorGenerator(back_img)
    plt.figure("wordc")
    plt.imshow(wc.recolor(color_func=image_colors))
    wc.to_file(res_full + '好友个性签名词云图.png')
    logger.info('end %s ' % func_name)


def snowlp_analysis(comment):
    """

    :param comment:
    :return:
    """
    func_name = "snow_analysis"
    logger.info('start %s ' % func_name)
    sentimentslist = []
    for li in comment:
        if len(li) > 0:
            s = SnowNLP(li)
            print(li, s.sentiments)
            sentimentslist.append(s.sentiments)
    fig1 = plt.figure("sentiment")
    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.02))
    plt.savefig(res_full + '好友签名情感分析')
    plt.show()
    logger.info('end %s ' % func_name)


def deal():
    """
    处理入口
    :return:
    """
    fri_infos = wc_login()
    sign_li = sign_words(fri_infos)
    word_cloud(sign_li)
    snowlp_analysis(sign_li)


if __name__ == '__main__':
    deal()
