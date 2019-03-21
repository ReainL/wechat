#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 19-3-18
@title: '配置'
@author: Xusl
"""
import os

# 其中 os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录
logger_path = os.path.join(os.path.dirname(__file__), 'logging.conf')







