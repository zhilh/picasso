#-*- coding:utf-8 -*-
import asyncio
import aiohttp
import time,os


# 异步并发客户端
class Asyncio_Client(object):

    def __init__(self):
        self.loop=asyncio.get_event_loop()
        self.tasks=[]

    # 将异步函数介入任务列表。后续参数直接传给异步函数
    def set_task(self,task_fun,num,*args):
        for i in range(num):
            self.tasks.append(task_fun(*args))

    # 运行，获取返回结果
    def run(self):
        back=[]
        try:
            f = asyncio.wait(self.tasks)   # 创建future
            self.loop.run_until_complete(f)  # 等待future完成
        finally:
            pass




# 服务器高并发压力测试
class Test_Load():

    total_time=0  # 总耗时
    total_payload=0  # 总负载
    total_num=0  # 总并发数
    all_time=[]

    # 创建一个异步任务，本地测试，所以post和接收几乎不损耗时间，可以等待完成，主要耗时为算法模块
    async def task_func1(self,session):

        begin = time.time()
        # print('开始发送：', begin)
        file=open(self.image, 'rb')
        print(file)
        fsize = os.path.getsize(self.image)
        self.total_payload+=fsize/(1024*1024)

        data = {"image_id": "2", 'image':file}
        r = await session.post(self.url,data=data)  #只post，不接收
        result = await r.json()
        self.total_num+=1
        # print(result)
        end = time.time()
        # print('接收完成：', end,',index=',self.total_num)
        self.all_time.append(end-begin)

    # 负载测试
    def test_safety(self):
        print('test begin')
        async_client = Asyncio_Client()  # 创建客户端
        session = aiohttp.ClientSession()
        for i in range(10):  # 执行10次
            self.all_time=[]
            self.total_num=0
            self.total_payload=0
            self.image = 'D:/work/face/img/20190315153956.png'  # 设置测试nayizhang
            print('测试图片：', self.image)
            begin = time.time()
            async_client.set_task(self.task_func1,self.total_num,session)  # 设置并发任务
            async_client.run()   # 执行任务

            end=time.time()
            self.all_time.sort(reverse=True)
            print(self.all_time)
            print('并发数量(个)：',self.total_num)
            print('总耗时(s)：',end-begin)
            print('最大时延(s)：',self.all_time[0])
            print('最小时延(s)：', self.all_time[len(self.all_time)-1])
            print('top-90%时延(s)：', self.all_time[int(len(self.all_time)*0.1)])
            print('平均耗时(s/个)：',sum(self.all_time)/self.total_num)
            print('支持并发率(个/s):',self.total_num/(end-begin))
            print('总负载(MB)：',self.total_payload)
            print('吞吐率(MB/S)：',self.total_payload/(end-begin))   # 吞吐率受上行下行带宽，服务器带宽，服务器算法性能诸多影响

            time.sleep(3)


        session.close()
        print('test finish')

t = Test_Load()
t.test_safety()


        
