#-*- coding:utf-8 -*-
'''
Created on 2018年8月29日
@author: zhilh
Description: 获取项目根目录路径
'''

import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))    #当前脚本所在目录
rootPath = os.path.split(curPath)[0]    #当前项目根目录
sys.path.append(rootPath)
#print(curPath,rootPath)

def get_cwd():
    path = os.path.dirname(os.path.abspath(__file__))
    #当前文件的绝对路径
    return path


