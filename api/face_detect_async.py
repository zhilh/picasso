#-*- coding:utf-8 -*-
'''
Created on 2019年6月11日
@author: zhilh
Description: 人脸识别接口压力测试--异步多并发
'''

import asyncio
from aiohttp import ClientSession, TCPConnector,ClientTimeout
import json
from datetime import datetime
import base64

 
#参数  
fileUrl='D:/work/face/img/IMG_201903.jpg'
url = 'http://172.13.2.163/vdinapi/face/v1/detect'
with open(fileUrl, 'rb') as f:  # 以二进制读取图片
    files = f.read()
    encodestr = base64.b64encode(files) # 得到 byte 编码的数据
    files=str(encodestr,'utf-8') # 重新编码数据
data={
    "appKey": "98e997dee93a9ba21a46fc897d633bfc"
     ,"appSecret": "eb63d2ab9abe36628579b29a5ca7672b"
     ,'imageBase64': "data:image/png;base64,"+files
    }
headers={
    #"Content-type": "multipart/form-data",
    "Accept": "text/plain"
    }

#data=json.dumps(data)#转换为json数据
all_Task_num = 500  #总共任务数
error = []  # 错误信息列表
Sem_num = 100 #并发数


async def post_api(session, i):
    start_time = datetime.now()
    try:
        async with session.post(url=url, data=data,headers=headers) as response:
            if response.status != 200:
                error.append(response.status)
            r = await response.read()
            end_time = datetime.now()
            cost = end_time-start_time
            msg = "第%d个请求，开始时间：%s, 花费时间: %s, 返回信息: %s\n" % (i, start_time, cost, r.decode())
            #print("running %d" % i, datetime.now())
    except Exception as e:
        #print("running %d,error %s" % (i,e))
        error.append('Exception')
        msg = "%d出问题了" % i + str(e) + "\n"
    print(msg)
    with open("../logs/faceDetect.log", "a+", encoding="utf-8") as f:
        f.write(msg)


async def _bound(sem, session, i):
    # 使用Semaphore， 它会在第一批2000个请求发出且返回结果(是否等待返回结果取决于你的接口API方法的定义)后
    # 检查本地TCP连接池(最大2000个)的空闲数(连接池某个插槽是否空闲，在这里，取决于请求是否返回)
    # 有空闲插槽，就PUT入一个请求并发出(完全不同于Jmeter的rame up in period的线性发起机制).
    # 所以，在结果log里，你会看到第一批请求(开始时间)是同一秒发起，而后面的则完全取决于服务器的吞吐量
    async with sem:
        await post_api(session, i)


async def run(task_num,Sem_num):
    tasks = []
    # Semaphore， 相当于基于服务器的处理速度和测试客户端的硬件条件，一批批的发直至发送完全部
    # 通常设置限制并发量为500, (windows最大506，linux是1024，超过会报错)
    sem = asyncio.Semaphore(Sem_num)
    # 创建session，且对本地的TCP连接不做限制limit=0
    # 超时时间指定
    # total:全部请求最终完成时间
    # connect: aiohttp从本机连接池里取出一个将要进行的请求的时间
    # sock_connect：单个请求连接到服务器的时间
    # sock_read：单个请求从服务器返回的时间
    timeout = ClientTimeout(total=300, connect=60, sock_connect=60, sock_read=60)
    async with ClientSession(connector=TCPConnector(limit=0), timeout=timeout) as session:
        for i in range(0, task_num):
            # 如果是分批的发，就使用并传递Semaphore
            task = asyncio.ensure_future(_bound(sem=sem,session=session, i=i))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses

def print_result(rst):
    for i in range(len(rst)):    
        r = json.loads(rst[i])#字符串转换为字典
        print(type(r),r)
        for key in r:
            print(key,':',r[key])

if __name__ == '__main__':
    start = datetime.now()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(all_Task_num,Sem_num))
    loop.run_until_complete(future)
    end = datetime.now()
    
    #取整数时间差（秒）：(end - start).seconds  
    #取小数后六位时间差（秒）：(end - start).total_seconds()  
    #时间差（微妙）(end - start).microseconds  
    
    print ("========================================================================")
    print ("接口性能测试开始时间：", start)
    print ("接口性能测试结束时间：", end)
    print ("接口地址：", url)
    print ("接口类型：Post")
    print ("请求任务总数：", all_Task_num)
    print ("并发数：", Sem_num)
    print ("错误数：", len(error))
    print ("总耗时（秒）：", (end-start).total_seconds())
    print ("每次请求耗时（秒）：",(end - start).total_seconds() / all_Task_num)
    print ("每秒承载请求数（TPS)：", all_Task_num / (end - start).total_seconds())
    

