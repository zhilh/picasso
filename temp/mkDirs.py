#-*- coding:utf-8 -*-
'''

Created on 2018年8月31日

@author: zhilh

部分常用函数
'''
import os



def mkdirs(path):
    ### 创建[多层]目录
    
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在；存在：True；不存在：False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)
        # 如果不存在则创建目录
        return True
    else:
        # 如果目录存在则不创建
        return False

    
