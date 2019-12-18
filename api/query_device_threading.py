#-*- coding:utf-8 -*-
'''
Created on 2019年6月5日
@author: zhilh
Description: 接口压力测试--多线程方案
'''

import requests
import time
import threading
import json

''' -------接口性能测试配置-------'''
method = "post" # 接口类型
#url = "http://192.168.0.130/vdinapi/face/v1/detect"  # 接口地址
#data = {"appKey": "98e997dee93a9ba21a46fc897d633bfc", "appSecret": "eb63d2ab9abe36628579b29a5ca7672b","imageData":"D:\work\face\img\IMG_201903.jpg"}    # 接口参数
#header={"Content-type": "multipart/form-data","Accept": "text/plain"}
data={'imei':'3033373900190028','userKey':'10CD1687A38642B19067E4941D6465E6'}
data=json.dumps(data)#转换为json数据
url='http://192.168.0.72:52001/lock/v1/querydevice'
header={"Content-type": "application/json", "Accept": "text/plain"}      
        
thread_num = 10000  # 线程数
one_work_num = 1    # 每个线程循环次数
loop_sleep = 0  # 每次请求时间间隔
response_time = []  # 平均响应时间列表
error = []  # 错误信息列表


class CreateThread:
    def __init__(self):
        pass

    @classmethod
    def thread_api(cls):
        '''接口函数'''
        global results
        try:
            if method == "post":
                results = requests.post(url, data,headers=header)
            if method == "get":
                results = requests.get(url, data,headers=header)
            #print(results.json())
            return results
        except requests.ConnectionError:
            return results

    @classmethod
    def thread_response(cls):
        ''' 获取响应时间 单位ms '''
        responsetime = float(CreateThread.thread_api().elapsed.microseconds) / 1000
        return responsetime

    @classmethod
    def thread_response_avg(cls):
        ''' 获取平均相应时间 单位ms '''
        avg = 0.000
        l = len(response_time)
        for num in response_time:
            avg += 1.000 * num / l
        return avg

    @classmethod
    def thread_time(cls):
        '''  获取当前时间格式 '''
        return time.asctime(time.localtime(time.time()))

    @classmethod
    def thread_error(cls):
        ''' 获取错误的返回状态码 '''
        if CreateThread.thread_api().status_code !=200 :
            error.append(CreateThread.thread_api().status_code)

    @classmethod
    def thread_work(cls):
        ''' 工作线程循环 '''
        threadname = threading.currentThread().getName()
        #print ("[", threadname, "] Sub Thread Begin")
        for i in range(one_work_num):
            CreateThread.thread_api()
            #print ("接口请求时间： ", CreateThread.thread_time())
            response_time.append(CreateThread.thread_response())
            CreateThread.thread_error()
            time.sleep(loop_sleep)
        #print ("[", threadname, "] Sub Thread End")

    @classmethod
    def thread_main(cls):
        start = time.time()
        threads = []
        for i in range(thread_num):
            t = threading.Thread(target=CreateThread.thread_work())
            t.setDaemon(True)
            threads.append(t)
        for t in threads:
            t.start()
        # 启动所有线程
        for t in threads:
            t.join()
        # 主线程中等待所有子线程退出
        end = time.time()

        print ("========================================================================")
        print ("接口性能测试开始时间：", time.asctime(time.localtime(start)))
        print ("接口性能测试结束时间：", time.asctime(time.localtime(end)))
        print ("接口地址：", url)
        print ("接口类型：", method)
        print ("线程数：", thread_num)
        print ("每个线程循环次数：", one_work_num)
        print ("每次请求时间间隔：", loop_sleep)
        print ("总请求数：", thread_num * one_work_num)
        print ("错误请求数：", len(error),error)
        print ("总耗时（秒）：", end - start)
        print ("每次请求耗时（秒）：", (end - start) / (thread_num * one_work_num))
        print ("每秒承载请求数（TPS)：", (thread_num * one_work_num) / (end - start))
        print ("平均响应时间（毫秒）：", CreateThread.thread_response_avg())


if __name__ == '__main__':
    CreateThread.thread_main()    
    
    
    