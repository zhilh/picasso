#-*- coding:utf-8 -*-
'''
Created on 2018年11月8日
@author: zhilh
Description: 存放一些简单算法封装函数
'''
import os,time
import win32clipboard as w
import win32con
import hashlib
import base64
from math import sin, asin, cos, radians, fabs, sqrt

from functools import wraps 
from contextlib import contextmanager

from datetime import datetime 
from datetime import timedelta


 
def getImgBase64(file_url):
    '''读取给定地址的图片（jpg、png），返回base64编码格式的图片数据'''
    with open(file_url, 'rb') as f:  # 以二进制读取图片
        files = f.read()
        encodestr = base64.b64encode(files) # 得到 byte 编码的数据
        files=str(encodestr,'utf-8') # 重新编码数据
    base64_ = "data:image/png;base64,"+files
    return base64_

def getMD5(str):
    '''生成MD5'''
    m = hashlib.md5()  
    # 此处必须声明encode, 否则报错为：hl.update(str)  Unicode-objects must be encoded before hashing
    m.update(str.encode(encoding="utf-8"))  
    return m.hexdigest() 
  
 
def excute_cmd_result(self,command):
    '''
    命令行运行输入的命令，返回运行结果
    '''
    result_list = []
    result = os.popen(command).readlines()
    for i in result:
        if i =='\n':
            continue
        result_list.append(i.strip('\n'))
    return result_list    
  
''''''
def hav(theta):
    s = sin(theta / 2)
    return s * s 
def get_distance_hav(lat0, lng0, lat1, lng1):
    "用haversine公式计算球面两点间的距离。"
    EARTH_RADIUS=6371           # 地球平均半径，6371km
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
 
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h)) 
    return distance
''''''

def get_clipBoard_text():
    '''
    获取剪切板内容
    '''
    w.OpenClipboard()
    t = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return t

def set_clipBoard_text(aString):
    '''
    写入剪切板内容
    '''
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT, aString)
    w.CloseClipboard()


def genMatrix(rows,cols):
    '''定义一个二维数组，默认都赋值：0
    多数用于列表list操作
    r,c=3,4
    lists=genMatrix(r,c)
    print(lists)
    for i in range(r):
        for j in range(c):
            print (i,j,': '+str(lists[i][j]))
    '''    
    matrix = [[0 for col in range(cols)] for row in range(rows)]
    return(matrix)


def mkDirs(path):
    '''创建[多层]目录'''
    
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在；存在：True；不存在：False
    isExists = os.path.exists(path) and os.path.isdir(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建
        return False

''''''
def testPass(self):
    '''用于unittest测试框架内，在case执行完成后，判断测试结果是否通过 '''
    if hasattr(self, '_outcome') :  # Python 3.4+
        result = self.defaultTestResult()  # these 2 methods have no side effects
        self._feedErrorsToResult(result, self._outcome.errors)
    else:  # Python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
        result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
        
    error = list2reason(self,result.errors)
    failure = list2reason(self,result.failures)        
    if not error and not failure:
        return True
    else:
        #typ, text = ('ERROR', error) if error else ('FAIL', failure)
        #msg = [x for x in text.split('\n')[1:] if not x.startswith(' ')][0]
        #print("\n%s: %s\n     %s" % (typ, self.id(), msg))
        return False
def list2reason(self, exc_list):
    if exc_list and exc_list[-1][0] is self:
        return exc_list[-1][1]
''''''

''''''
# 测试一个函数的运行时间，使用方式：在待测函数直接添加此修饰器
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('\n============================================================')
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        print('============================================================\n')
        return r
    return wrapper


# 测试一段代码运行的时间，使用方式：上下文管理器with
# with timeblock('block_name'):
#     your_code_block...
@contextmanager
def timeblock(label='Code'):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print('==============================================================')
        print('{} run time: {}'.format(label, end - start))
        print('==============================================================')



class AutoTask():
    '''简单的自动执行任务控制'''
    def __init__(self):
        pass
    def __del__(self):
        pass
    def run_task(self,_func, _day=0, _hour=0, _min=0, _sec=0):  
        '''        
        控制在间隔多少秒（或者分钟、小时、天）后执行一个任务
         没有输入间隔时间，则只运行一次
         调用方式
        def works():
            os.system('test1.py')
        
        at=AutoTask()
        at.run_task(works,_sec=10)           
        '''
        # Init time  
        now = datetime.now()
        strnow = now.strftime('%Y-%m-%d %H:%M:%S')
        print("now:",strnow)
        # First next run time  
        period = timedelta(days=_day, hours=_hour, minutes=_min, seconds=_sec)  
        next_time = now  
        strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')  
        print("next run:",strnext_time)  
        print('--------------')
        
        while True:  
            # Get system current time  
            iter_now = datetime.now()  
            iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S') 
            #print(iter_now_time,strnext_time) 
            if str(iter_now_time) >= str(strnext_time):  
                # Get every start work time  
                print("start work: %s" % iter_now_time)  
                # Call task func 
                _func()  
                print("task done.")  
                
                if (_day==0 and _hour==0 and _min==0 and _sec==0):
                    break
                # Get next iteration time  
                iter_time = datetime.now() + period  
                strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')  
                print("next_iter: %s" % strnext_time)
                print('--------------')
                # Continue next iteration  
                #continue
            time.sleep(1)
    


