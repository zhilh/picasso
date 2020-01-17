#-*- coding:utf-8 -*-
'''
Created on 2020年1月3日
@author: zhilh
Description: 
通过paramiko模块，获取远程Linux设备的内存、cpu、磁盘、网络等信息
'''

from framework.sshhd import SSHhandle
import re,time

#设置主机列表
HOST_LIST=(
    {'ip':'192.168.0.197', 'port':22, 'username':'root', 'password':'qwe123'},
    #{'ip':'192.168.0.197', 'port':22, 'username':'root', 'password':'qwe123'},
    )

def get_memory_info():
    '''
    内存信息的读取:
    通过远程执行‘cat /proc/meminfo’可以获取内存相关信息。
    这里我们只读取MemTotal和MemFree的信息。需要读取其他信息可以利用正则表达式匹配获取其他数据。
    例如把这两个信息输出到标准输出中，实际应用可以通过crontab定时执行脚本，把结果写入文件，可以给传给监控系统，当超越一定阀值的时候进行相应的处理
    '''
    for host in HOST_LIST:
        ssh=SSHhandle(host=host['ip'], port=host['port'], username=host['username'], password=host['password'])
        ssh.connect()
        print(host['ip'])
        stdin, stdout, stderr = ssh.exc_cmd('cat /proc/meminfo')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        
        if str_err != "":
            print(str_err)
            continue
        #print(str_out)
        
        str_total = re.search('MemTotal:.*?\n', str_out).group()
        print(str_total)
        totalmem = re.search('\d+',str_total).group()
        
        str_free = re.search('MemFree:.*?\n', str_out).group()
        print(str_free)
        freemem = re.search('\d+',str_free).group()
        use = round(float(freemem)/float(totalmem), 2)
        print('当前内存使用率为：', str(use))
        ssh.close()

def get_cpu_info():
    '''
    CPU使用率的读取:
    这里使用cat /proc/stat命令读取实时的CPU使用率。
    由于这个时间数值是从开机之后一直累加的，因此我们要取一次值之后，隔一小段时间再取一次值，前后两次的值相减，再计算这段时间的CPU利用率。具体公式是：
    CPU利用率= 1-(CPU空闲时间2 - CPU空闲时间1) / (CPU总时间2 - CPU总时间1)
    其中"CPU空闲时间1"为第一次取值时第4项的值，"CPU空闲时间2"为第二次取值时第4项的值，"CPU总时间1"为第一次取值时各项数值的总和，"CPU总时间2"为第二次取值时各项数值的总和
    '''
    for host in HOST_LIST:
        ssh=SSHhandle(host=host['ip'], port=host['port'], username=host['username'], password=host['password'])
        ssh.connect()
        print(host['ip'])
        stdin, stdout, stderr = ssh.exc_cmd('cat /proc/stat | grep "cpu "')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
     
        if str_err != "":
            print(str_err)
            continue
        else:
            cpu_time_list = re.findall('\d+', str_out)
            cpu_idle1 = cpu_time_list[3]
            total_cpu_time1 = 0
            for t in cpu_time_list:
                total_cpu_time1 = total_cpu_time1 + int(t)
     
        time.sleep(2)
     
        stdin, stdout, stderr = ssh.exc_cmd('cat /proc/stat | grep "cpu "')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        if str_err != "":
            print(str_err)
            continue
        else:
            cpu_time_list = re.findall('\d+', str_out)
            cpu_idle2 = cpu_time_list[3]
            total_cpu_time2 = 0
            for t in cpu_time_list:
                total_cpu_time2 = total_cpu_time2 + int(t)
     
        cpu_usage = round(1 - (float(cpu_idle2) - float(cpu_idle1)) / (total_cpu_time2 - total_cpu_time1), 2)
        print('当前CPU使用率为：' + str(cpu_usage))
        ssh.close()

def get_disk_info():
    '''
    磁盘使用率
    这里使用df命令获取磁盘使用情况。该命令既获取了磁盘的容量，也获取了使用率，可以根据需要进行后续的处理        
    '''    
    for host in HOST_LIST:
        ssh=SSHhandle(host=host['ip'], port=host['port'], username=host['username'], password=host['password'])
        ssh.connect()
        print(host['ip'])
        stdin, stdout, stderr = ssh.exc_cmd('df -lm')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        
        if str_err != "":
            print(str_err)
            continue
        
        print('磁盘使用率为：'+str(str_out))    
        ssh.close()
        
        
def get_network_info():
    '''
    网络流量
    这里使用cat /proc/net/dev查看网络流量。该命令既获取了磁盘的容量，也获取了使用率，可以根据需要进行后续的处理        
    '''    
    for host in HOST_LIST:
        ssh=SSHhandle(host=host['ip'], port=host['port'], username=host['username'], password=host['password'])
        ssh.connect()
        print(host['ip'])
        stdin, stdout, stderr = ssh.exc_cmd('cat /proc/net/dev')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        
        if str_err != "":
            print(str_err)
            continue
        
        print('网络流量为：'+str(str_out))    
        ssh.close()
        
def test():
    get_memory_info()
    get_cpu_info()
    get_disk_info()
    get_network_info()
 
if __name__ == '__main__':
    test()

        
        