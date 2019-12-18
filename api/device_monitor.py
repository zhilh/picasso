#-*- coding:utf-8 -*-
'''
Created on 2019年5月9日
@author: zhilh
Description: 设备监控，监控指标：
    1、在线状态，通过ping实现
'''
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from framework.func import AutoTask
from framework.Execl import ExcelReader,ExcelAdd
from framework import  log
from framework.Email import SendEmail
import getcwd

import subprocess
import re


def get_ping_result(ip_address):
    p = subprocess.Popen(["ping.exe", ip_address], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    out = p.stdout.read().decode('gbk')
    #print(out)
    
    reg_receive = '已接收 = \d'
    match_receive = re.search(reg_receive, out)
    
    receive_count = -1
    
    if match_receive:
        receive_count = int(match_receive.group()[6:])
    
    if receive_count > 0:    #接受到的反馈大于0，表示网络通
        reg_min_time = '最短 = \d+ms'
        reg_max_time = '最长 = \d+ms'
        reg_avg_time = '平均 = \d+ms'
        
        match_min_time = re.search(reg_min_time, out)
        if match_min_time==None:
            min_time=''
        else:
            min_time = int(match_min_time.group()[5:-2])
        
        match_max_time = re.search(reg_max_time, out)
        if match_max_time==None:
            max_time=''
        else:        
            max_time = int(match_max_time.group()[5:-2])
        
        match_avg_time = re.search(reg_avg_time, out)
        if match_avg_time==None:
            avg_time=''
        else:        
            avg_time = int(match_avg_time.group()[5:-2])
        log.info('ping到达目标服务器<%s>！'%ip_address)
        return [receive_count, min_time, max_time, avg_time]
    else:
        log.info('网络不通，目标服务器<%s>不可达！'%ip_address)
        return [0, 9999, 9999, 9999]
    
def works():    
    execlName=os.path.join(getcwd.get_cwd(),"data\\device_ip.xls")
    reader = ExcelReader(execlName, sheet='test_ip',title_line=False)
    data_table=reader.data
    log.info('Execl文件读取成功')
    writer_table=ExcelAdd(execlName,sheet='test_ip')
    col_Num=writer_table.get_cols()
    writer_table.modify_cell(0, col_Num, 'receive_count')
    writer_table.modify_cell(0, col_Num+1, 'min_time')
    writer_table.modify_cell(0, col_Num+2, 'max_time')
    writer_table.modify_cell(0, col_Num+3, 'avg_time')
    log.info('Execl文件表头写入成功')
    
    failed = 0
    for i in range(1,len(data_table)):
        ip=data_table[i][1]
        ping=get_ping_result(ip)
        receive_count=ping[0]
        min_time=ping[1]
        max_time=ping[2]
        avg_time=ping[3]
        
        if receive_count == 0 :
            failed = failed + 1
        if min_time=='' and max_time=='' and avg_time=='':
            failed = failed + 1
        writer_table.modify_cell(i, col_Num, receive_count)
        writer_table.modify_cell(i, col_Num+1, min_time)
        writer_table.modify_cell(i, col_Num+2, max_time)
        writer_table.modify_cell(i, col_Num+3, avg_time)
    ret_file=writer_table.save('test112.xls')
    log.info('Execl文件数据保存成功<%s>'%ret_file)

    if failed > 0 :
        mail=SendEmail()
        mail.send_mail(
            files=[ret_file],
            subject='注意：监控的设备列表中有设备不在线'
            )

if __name__ == "__main__":
    #pass
    at=AutoTask()
    at.run_task(works,_day=0,_hour=12,_min=0,_sec=0)  

