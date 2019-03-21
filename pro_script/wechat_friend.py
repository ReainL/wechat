#!/usr/bin/env python3.5
# encoding: utf-8
"""
Created on 19-3-18
@title: '探索好友性别比例饼图'
@author: Xusl
"""
import os
import logging.config
import matplotlib.pyplot as plt

from config import logger_path
from pro_script.wechat_login import wc_login

logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")


def sex_ratio(fri_infos):
    """
    好友性别比例
    :param fri_infos:
    :return:
    """
    func_name = "好友性别比例"
    logger.info('start %s ' % func_name)
    total = len(fri_infos)   # 好友总数量
    man = 0
    woman = 0
    other = 0

    for fri_info in fri_infos:
        sex = fri_info['sex']
        # 如果sex=1 代表男性 sex=2代表女性
        if sex == 1:
            man += 1
        elif sex == 2:
            woman += 1
        else:
            other += 1

    man_ratio = int(man)/total * 100
    woman_ratio = int(woman)/total * 100
    other_ratio = int(other)/total * 100
    plt.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.figure(figsize=(5, 5))  # 绘制的图片为正圆
    sex_li = ['男', '女', '其他']
    radius = [0.01, 0.01, 0.01]  # 设定各项距离圆心n个半径
    colors = ['red', 'yellowgreen', 'lightskyblue']
    proportion = [man_ratio, woman_ratio, other_ratio]

    logger.debug('proportion:%s' % proportion)

    plt.pie(proportion, explode=radius, labels=sex_li, colors=colors, autopct='%.2f%%')   # 绘制饼图
    # 加入图例 loc =  'upper right' 位于右上角 bbox_to_anchor=[0.5, 0.5] # 外边距 上边 右边 borderaxespad = 0.3图例的内边距
    plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.1), borderaxespad=0.3)

    plt.title('微信好友性别比例')    # 绘制标题
    # 获取上一层目录
    pwd_path = os.path.abspath(os.path.dirname(os.getcwd()))
    desc_full = os.path.join(pwd_path, 'res')
    plt.savefig(desc_full + '/微信好友性别比例')    # 保存图片
    plt.show()
    logger.info('end %s ' % func_name)


def deal():
    """
    处理入口
    :return:
    """
    fri_infos = wc_login()
    sex_ratio(fri_infos)


if __name__ == '__main__':
    deal()

