#-*- coding:utf-8 -*-
'''
Created on 2019年7月25 日
@author: zhilh
Description: 注册接口压力测试--异步通讯方案
'''

import asyncio
from aiohttp import ClientSession, TCPConnector,ClientTimeout
import json
from datetime import datetime
from framework import rdData
from framework import func

 
#参数  
'''
url = 'http://192.168.0.243:8848/api/v1/ftr/register?app_key=39759b11c05e80ecb6056e86a9126228&time=1563876416&sign=EDC26F90C7471159CCB8B6ADBD6DD7E3'
data={
    'machineCode':'r86jsjak2asdfLJWEHh0985jldlfg342'
    }
data=json.dumps(data)#转换为json数据
'''
header={
    "Content-type": "application/json"
    , "Accept": "text/plain"
    }
all_Task_num = 1  #总共任务数
error = []  # 错误信息列表

async def test_api(session, i):
    start_time = datetime.now()
    try:
        data={
            'machineCode':rdData.getStrings(32)
            }
        data=json.dumps(data)
        t_=rdData.getTimestamp()
        strA="app_key=39759b11c05e80ecb6056e86a9126228&app_secret=888759975E497AcA8C5f627B188ba5ae&time="+t_
        sign_= func.getMD5(strA).upper()
        url = 'http://192.168.0.243:8848/api/v1/ftr/register?app_key=39759b11c05e80ecb6056e86a9126228&time='+t_+'&sign='+sign_
        #print(url)
        async with session.post(url=url, data=data, headers=header) as response:
            if response.status != 200:
                error.append(response.status)
            r = await response.read()
            end_time = datetime.now()
            cost = end_time-start_time
            msg = "第%d个注册请求，开始时间：%s, 花费时间: %s, 返回信息: %s\n" % (i, start_time, cost, r.decode())
            #print("running %d" % i, datetime.now())
    except Exception as e:
        #print("running %d,error %s" % (i,e))
        msg = "%d出问题了" % i + str(e) + "\n"
    with open("../logs/register.log", "a+", encoding="utf-8") as f:
        f.write(msg)


async def _bound(sem, session, i):
    # 使用Semaphore， 它会在第一批2000个请求发出且返回结果(是否等待返回结果取决于你的接口API方法的定义)后
    # 检查本地TCP连接池(最大2000个)的空闲数(连接池某个插槽是否空闲，在这里，取决于请求是否返回)
    # 有空闲插槽，就PUT入一个请求并发出(完全不同于Jmeter的rame up in period的线性发起机制).
    # 所以，在结果log里，你会看到第一批请求(开始时间)是同一秒发起，而后面的则完全取决于服务器的吞吐量
    async with sem:
        await test_api(session, i)


async def run(num):
    tasks = []
    # Semaphore， 相当于基于服务器的处理速度和测试客户端的硬件条件，一批批的发直至发送完全部
    # 通常设置限制并发量为500, (windows最大506，linux是1024，超过会报错)
    sem = asyncio.Semaphore(500)
    # 创建session，且对本地的TCP连接不做限制limit=0
    # 超时时间指定
    # total:全部请求最终完成时间
    # connect: aiohttp从本机连接池里取出一个将要进行的请求的时间
    # sock_connect：单个请求连接到服务器的时间
    # sock_read：单个请求从服务器返回的时间
    timeout = ClientTimeout(total=300, connect=60, sock_connect=60, sock_read=60)
    async with ClientSession(connector=TCPConnector(limit=0), timeout=timeout) as session:
        for i in range(0, num):
            # 如果是分批的发，就使用并传递Semaphore
            task = asyncio.ensure_future(_bound(sem=sem,session=session, i=i))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses

if __name__ == '__main__':
    start = datetime.now()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(all_Task_num))
    loop.run_until_complete(future)
    end = datetime.now()
    
    #取整数时间差（秒）：(end - start).seconds  
    #取小数后六位时间差（秒）：(end - start).total_seconds()  
    #时间差（微妙）(end - start).microseconds  
    
    print ("========================================================================")
    print ("接口性能测试开始时间：", start)
    print ("接口性能测试结束时间：", end)
    #print ("接口地址：", url)
    print ("接口类型：Post")
    print ("请求任务总数：", all_Task_num)
    print ("错误请求数：", len(error),error)
    print ("总耗时（秒）：", (end-start).total_seconds())
    print ("每次请求耗时（秒）：",(end - start).total_seconds() / all_Task_num)
    print ("每秒承载请求数（TPS)：", all_Task_num / (end - start).total_seconds())
    

