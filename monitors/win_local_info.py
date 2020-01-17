#-*- coding:utf-8 -*-
'''
Created on 2019年12月31日
@author: zhilh
Description: 
    获取Windows系统设备的监控信息
    CPU、memory、disk

'''


import psutil

cpu_info={'user':0,  'system':0,  'idle':0,   'percent':0}
memory_info={'total':0, 'available':0,  'percent':0,  'used':0, 'free':0}
disk_id =   []
disk_total=[]
disk_used=[]
disk_free=[]
disk_percent=[]


#get cpu information
def get_cpu_info():
    cpu_times = psutil.cpu_times()
    cpu_info['user']    =   cpu_times.user
    cpu_info['system']  =   cpu_times.system
    cpu_info['idle']    =   cpu_times.idle
    cpu_info['percent'] =   psutil.cpu_percent(interval=2)

#get memory information
def get_memory_info():
    mem_info = psutil.virtual_memory()
    memory_info['total']    =   mem_info.total
    memory_info['available']    =   mem_info.available
    memory_info['percent']    =   mem_info.percent
    memory_info['used']    =   mem_info.used
    memory_info['free']    =   mem_info.free

def get_disk_info():
    for id in   psutil.disk_partitions():  
        if  'cdrom' in  id.opts or  id.fstype   =='':
            continue
        disk_name   =   id.device.split(':')
        s   =   disk_name[0]
        disk_id.append(s)
        disk_info   =   psutil.disk_usage(id.device)
        disk_total.append(disk_info.total)
        disk_used.append(disk_info.used)
        disk_free.append(disk_info.free)
        disk_percent.append(disk_info.percent)        


if  __name__    ==   '__main__':
    get_cpu_info()
    print(cpu_info)
    cpu_status = cpu_info['percent']
    print('cpu usage is:%s%%'    %cpu_status)

    get_memory_info()
    print(memory_info)
    mem_status = memory_info['percent']
    print('memory usage is:%s%%' %mem_status)

    get_disk_info()
    for i   in  range(len(disk_id)):
        print('%s   disk usage is:%s%%'  %(disk_id[i], 100 - disk_percent[i]))
