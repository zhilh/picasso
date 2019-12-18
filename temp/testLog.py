#-*- coding:utf-8 -*-
'''
Created on 2018年9月28日
@author: zhilh
Description: 
'''

 
from framework import log


def test():
    
    log.debug('hello, world,这是一个debug信息')
    log.info('hello, world,这是一个info信息')
    log.warning('hello ,world,这是一个warning信息')
    log.exception('hello ,world,这是一个exception信息')
    log.error('hello, world,这是一个error信息')
    log.critical('hello, world,这是一个critical信息')
  
if __name__ == "__main__":
    test()