#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 19-3-19
@title: '微信好友区域Top10'
@author: Xusl
"""
import os
import logging.config
import matplotlib.pyplot as plt

from config import logger_path
from pro_script.wechat_login import wc_login

logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")


def area_top10(fri_infos):
    """
    好友性别比例
    :param fri_infos:
    :return:
    """
    func_name = "微信好友区域Top10"
    logger.info('start %s ' % func_name)
    prov_dict, city_dict = {}, {}
    for fri_info in fri_infos:
        prov = fri_info['province']
        city = fri_info['city']
        if prov and prov not in prov_dict.keys():
            prov_dict[prov] = 1
        elif prov:
            prov_dict[prov] += 1
        if city and city not in city_dict.keys():
            city_dict[city] = 1
        elif city:
            city_dict[city] += 1

    prov_dict_top10 = sorted(prov_dict.items(), key=lambda x: x[1], reverse=True)[0:10]
    city_dict_top10 = sorted(city_dict.items(), key=lambda y: y[1], reverse=True)[0:10]
    logger.debug('prov_dict_top10: %s' % prov_dict_top10)
    logger.debug('city_dict_top10: %s' % city_dict_top10)

    prov_nm, prov_num = [], []  # 省会名 + 数量
    for prov_data in prov_dict_top10:
        prov_nm.append(prov_data[0])
        prov_num.append(prov_data[1])

    pwd_path = os.path.abspath(os.path.dirname(os.getcwd()))
    desc_full = os.path.join(pwd_path, 'res')
    colors = ['#00FFFF', '#7FFFD4', '#F08080', '#90EE90', '#AFEEEE',
              '#98FB98', '#B0E0E6', '#00FF7F', '#FFFF00', '#9ACD32']
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    index = range(len(prov_num))
    plt.bar(index, prov_num, color=colors, width=0.5, align='center')

    plt.xticks(range(len(prov_nm)), prov_nm)  # 横坐轴标签
    for x, y in enumerate(prov_num):
        # 在柱子上方1.2处标注值
        plt.text(x, y + 1.2, '%s' % y, ha='center', fontsize=10)
    plt.ylabel('省会好友人数')  # 设置纵坐标标签
    prov_title = '微信好友区域Top10'
    plt.title(prov_title)    # 设置标题
    plt.savefig(desc_full + '/微信好友区域Top10')  # 保存图片

    city_nm, city_num = [], []  # 城市 + 数量
    for city_data in city_dict_top10:
        city_nm.append(city_data[0])
        city_num.append(city_data[1])

    index = range(len(city_num))
    plt.bar(index, city_num, color=colors, width=0.5, align='center')

    plt.xticks(range(len(city_nm)), city_nm)    # 横坐轴标签
    plt.ylabel('城市好友人数')  # 设置纵坐标标签
    city_title = '微信好友城市Top10'
    plt.title(city_title)       # 设置标题
    plt.savefig(desc_full + '/微信好友城市Top10')
    # 显示
    plt.show()
    logger.info('end %s ' % func_name)


def deal():
    """
    处理入口
    :return:
    """
    fri_infos = wc_login()
    area_top10(fri_infos)


if __name__ == '__main__':
    deal()
