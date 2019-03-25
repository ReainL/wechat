#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 19-3-25
@title: '微信群好友信息分析'
@author: Xusl
"""
import os
import itchat
import pandas as pd
import logging.config
import matplotlib.pyplot as plt

from config import logger_path
from pro_script.wechat_login import wc_login

logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")


def grp_sex_ratio(grp_nm, ):
    """
    群好友性别比例
    :param grp_nm: 想获取群聊信息的群名
    :return:
    """
    func_name = "群好友性别"
    logger.info('start %s ' % func_name)
    df_member = pd.read_csv("df_member.csv")
    mem_sex = dict(df_member['Sex'].replace({1: '男', 2: '女', 0: '其他'}).value_counts(normalize=True))    # 使用pandas库自带的统计值函数
    sex_li = []
    proportion = []
    for key, value in mem_sex.items():
        sex_li.append(key)
        proportion.append(format(value, '.2'))

    plt.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.figure(figsize=(5, 5))  # 绘制的图片为正圆
    sex_li = ['男', '女', '其他']
    radius = [0.01, 0.01, 0.01]  # 设定各项距离圆心n个半径
    colors = ['red', 'yellowgreen', 'lightskyblue']
    logger.debug('proportion:%s' % proportion)

    plt.pie(proportion, explode=radius, labels=sex_li, colors=colors, autopct='%.2f%%')   # 绘制饼图
    # 加入图例 loc =  'upper right' 位于右上角 bbox_to_anchor=[0.5, 0.5] # 外边距 上边 右边 borderaxespad = 0.3图例的内边距
    plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.1), borderaxespad=0.3)

    plt.title(grp_nm + '群好友性别比例')    # 绘制标题
    # 获取上一层目录
    pwd_path = os.path.abspath(os.path.dirname(os.getcwd()))
    desc_full = os.path.join(pwd_path, 'res')
    plt.savefig(desc_full + '/' + grp_nm + '好友性别比例')    # 保存图片
    plt.show()
    logger.info('end %s ' % func_name)


def grp_city(grp_nm):
    """
    群好友城市比例
    :param grp_nm: 想获取群聊信息的群名
    :return:
    """
    func_name = "群好友城市比例"
    logger.info('start %s ' % func_name)
    df_member = pd.read_csv("df_member.csv")
    df_member = df_member['DisplayName'].values
    mem_nm_li = []
    for mem_nm in df_member:
        if mem_nm:
            mem_nm = str(mem_nm).replace('  ', '')
            mem_nm = mem_nm.replace('一', '-').replace('_', '-').replace('－', '-').replace(' ', ' ')\
                .replace(' ', '-').replace('~', '-').replace('—', '-').replace('+', '-').replace('～','-')
            mem_nm = mem_nm.replace('--', '-')
            mem_nm_li.append(mem_nm)
    logger.debug('mem_nm_li：%s' % mem_nm_li)

    city_dict, industry_dict = {}, {}
    for per_info in mem_nm_li:
        split_num = per_info.count("-", 0, len(per_info))
        if split_num == 2:
            nm, city, industry = per_info.split('-')
            if city and city not in city_dict.keys():
                city_dict[city] = 1
            elif city:
                city_dict[city] += 1

    logger.debug('city_dict：%s' % city_dict)
    city_dict_top20 = sorted(city_dict.items(), key=lambda x: x[1], reverse=True)[0:20]

    city_nm, city_num = [], []  # 城市名 + 数量
    for prov_data in city_dict_top20:
        city_nm.append(prov_data[0])
        city_num.append(prov_data[1])
    pwd_path = os.path.abspath(os.path.dirname(os.getcwd()))
    desc_full = os.path.join(pwd_path, 'res')
    colors = ['#00FFFF', '#7FFFD4', '#F08080', '#90EE90', '#AFEEEE',
              '#98FB98', '#B0E0E6', '#00FF7F', '#FFFF00', '#9ACD32',
              '#00FFFF', '#7FFFD4', '#F08080', '#90EE90', '#AFEEEE',
              '#98FB98', '#B0E0E6', '#00FF7F', '#FFFF00', '#9ACD32'
              ]
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    index = range(len(city_num))
    plt.bar(index, city_num, color=colors, width=0.5, align='center')

    plt.xticks(range(len(city_nm)), city_nm, fontsize=8)  # 横坐轴标签
    for x, y in enumerate(city_num):
        # 在柱子上方1.0处标注值
        plt.text(x, y + 1.0, '%s' % y, ha='center', fontsize=10)
    plt.ylabel('群好友人数')  # 设置纵坐标标签
    prov_title = '中产之路2群(新)群好友人数Top20'
    plt.title(prov_title)  # 设置标题
    plt.savefig(desc_full + '/中产之路2群(新)群好友人数Top20')  # 保存图片
    logger.info('end %s ' % func_name)


def deal():
    """
    处理入口
    :return:
    """
    wc_login()
    # grp_lost = itchat.get_chatrooms() # 获取所有群聊信息
    grp_nm = '中产之路2群(新)'
    mid_road = itchat.search_chatrooms(name=grp_nm)  # 获取群聊名为中产之路2群(新)的群好友信息
    # 群聊用户列表的获取方法为update_chatroom, detailedMember=True将返回指定用户的信息组成的列表
    member_list = itchat.update_chatroom(mid_road[0]['UserName'], detailedMember=True)
    df_member = pd.DataFrame(member_list['MemberList'])  # 将用户信息转化为dateFrame格式
    df_member.to_csv('df_member.csv')
    grp_sex_ratio(grp_nm)
    grp_city(grp_nm)


if __name__ == '__main__':
    deal()
