#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 19-3-19
@title: '微信登录'
@author: Xusl
"""
import itchat


def wc_login():
    """
    登录
    :return:
    """
    itchat.auto_login(hotReload=True)
    itchat.dump_login_status()
    we_friend = itchat.get_friends(update=True)[:]
    friend_infos = []

    for friend in we_friend[1:]:
        nick_name = friend["NickName"]  # 好友昵称
        sex = friend["Sex"]  # 性别
        remark_name = friend["RemarkName"]  # 备注
        signature = friend["Signature"]  # 个性签名
        province = friend["Province"]  # 省份
        city = friend["City"]  # 城市

        friend_infos.append({
            'nick_name': nick_name,
            'sex': sex,
            'remark_name': remark_name,
            'signature': signature,
            'province': province,
            'city': city,
        })
    return friend_infos
