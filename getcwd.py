#-*- coding:utf-8 -*-
'''
Created on 2018年8月29日
@author: zhilh
Description: 获取项目根目录路径
'''

import os


def get_cwd():
    path = os.path.dirname(os.path.abspath(__file__))
    #当前文件的绝对路径
    return path


