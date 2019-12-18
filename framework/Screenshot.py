#-*- coding:utf-8 -*-
'''

Created on 2018年8月31日

@author: zhilh

'''
import os
import time
import getcwd
from framework.func import mkDirs

'''
在selenium中，使用driver.get_screenshot_as_file方法截图
在appium只，使用driver.save_screenshot方法截图
截图按照每天创建文件夹，日期+时间+自定义名称为文件名
默认报错到项目根目录的screenshots文件夹下
'''
class Screenshot(object):
    def __init__(self, my_driver):
        self.driver = my_driver

    #savePngName:生成图片的名称
    def savePngName(self, Spath='screenshots',Sname='temp'):
        """
        Sname：自定义图片的名称
        Spath：图片路径
        """
        proj_path=getcwd.get_cwd()
        img_path = os.path.join(proj_path, Spath, time.strftime('%Y-%m-%d', time.localtime(time.time())))#拼接文件路径
        img_path = img_path.replace("/","//")
        img_path = img_path.replace("\\","//")
        #print(img_path)
        mkDirs(img_path)#如果没有这个文件夹就新建
       
        img_type='.png'   
        img_name= time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) 
        img_name =img_name+"_"+Sname+img_type
        
        re_name=os.path.join(img_path,img_name)
        try:
            self.driver.get_screenshot_as_file(re_name)
            return re_name
        except NameError as e:
            print(e)
            return False


    
    