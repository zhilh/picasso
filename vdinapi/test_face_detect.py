#-*- coding:utf-8 -*-
'''
Created on 2019年5月9日
@author: zhilh
Description: 接口测试--接口功能测试
    测试用例由execl提供，测试结果回写到execl
'''
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
projPath = os.path.split(curPath)[0]
sys.path.append(projPath)

from framework.func import AutoTask
from framework.Execl import ExcelReader,ExcelAdd
from framework import  log
from framework.Email import SendEmail
from framework.func import getImgBase64
import getcwd
import requests
import json
    
def works():    
    execlName=os.path.join(getcwd.get_cwd(),"data\\face_detect.xls")
    reader = ExcelReader(execlName, sheet='face_detect',title_line=False)
    data_table=reader.data
    log.info('Execl文件读取成功')
    writer_table=ExcelAdd(execlName,sheet='face_detect')
    col_Num=writer_table.get_cols()
    writer_table.modify_cell(0, col_Num, 'status')
    writer_table.modify_cell(0, col_Num+1, 'return_msg')
    log.info('Execl文件表头写入成功')
    
    failed = 0
    for i in range(1,len(data_table)):
        imgUrl=data_table[i][0]
        apiUrl=data_table[i][1]
        appKey=data_table[i][2]
        appSecret=data_table[i][3]
        
        datas={
            "appKey": appKey
             ,"appSecret": appSecret
             ,'imageBase64': getImgBase64(imgUrl)
            }
        datas=json.dumps(datas)#转换为json数据
        headers={
            #"Content-type": "multipart/form-data",
            "Accept": "text/plain"
            }
        header={
            "Content-type": "application/json", 
            "Accept": "text/plain",
            "charset": "UTF-8"
            }
        
       
        #r = requests.post(apiUrl,data=datas,headers=headers) 
        #json_data = r.json()
        #print(type(r.json_data()),r.json_data())
        json_data=apiUrl
        print('接口返回结果：',apiUrl)
        
        writer_table.modify_cell(i, col_Num, 'debug')
        writer_table.modify_cell(i, col_Num+1, json_data)
    ret_file=writer_table.save()
    log.info('Execl文件数据保存成功<%s>'%ret_file)

    if failed > 110 :
        mail=SendEmail()
        mail.send_mail(
            files=[ret_file],
            subject='注意：接口测试中有部分case测过未通过'
            )

if __name__ == "__main__":
    works()
    #pass
    #at=AutoTask()
    #at.run_task(works,_day=0,_hour=12,_min=0,_sec=0)  

