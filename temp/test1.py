#-*- coding:utf-8 -*-
'''

Created on 2018年8月31日

@author: zhilh

'''
def a(s):
    print (s)
def switch(ch):
    try:
        {
        '1': lambda : a("one"),
        '2': lambda : a("two"),
        '3': lambda : a("three"),
        'a': lambda : a("Letter a")
        }[ch]()
    except KeyError:
        a("Key not Found")
      
#switch('ad')

import sys
 
def fibonacci(n): # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n): 
            return
        yield a
        a, b = b, a + b
        counter += 1
f = fibonacci(10) # f 是一个迭代器，由生成器返回生成
 
while True:
    try:
        print (next(f), end=" ")
    except StopIteration:
        sys.exit()
        
        
        
        
        
    