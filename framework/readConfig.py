#-*- coding:utf-8 -*-
'''

Created on 2018年9月28日

@author: zhilh

'''
from framework import log
import configparser
import getcwd
import os


configPath = os.path.join(getcwd.get_cwd(),'config', "config.ini") 

class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_config(self, field, key):
        '''获取config.ini信息'''
        result = self.cf.get(field, key)
        # log.debug('%s的%s是：%s' % (field, key, result))
        return result

    def set_config(self, field, key, value):
        '''修改config.ini信息'''
        fd = open(configPath, "w")
        self.cf.set(field, key, value)
        self.cf.write(fd)
        log.info('%s的%s修改成功 ,value=%s' % (field, key, value))


def test():
    config = ReadConfig()
    print(config.get_config("QUJINGACCOUNT", "login_url"))
    config.set_config("EMAIL", "on_off", "1")
    
if __name__ == '__main__':
    test()
    
    
    