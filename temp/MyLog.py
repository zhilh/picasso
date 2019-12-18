#-*- coding:utf-8 -*-
'''
Created on 2018年8月29日
@author: zhilh
Description: 
'''

import logging 
import os  
import getcwd
from framework.mkDirs import mkdirs
  
class Logger(object):  
    '''
    日志记录模块封装，支持自定义日志路径，自定义日志文件名
    '''
    def __init__(self, logPath="Logs",logName="log.txt"):  
        #定义路径, logPath='..\tmp\logs' 
        #创建文件,logName='log.txt'
        #默认在这个文件相同路径下创建logs文件夹，在logs文件夹下创建log.txt文件
        #cur_path = os.path.dirname(os.path.realpath(__file__))#当前文件路径
        proj_path=getcwd.get_cwd()#项目根目录路径，默认在项目根目录下创建日志文件夹
        
        log_path = os.path.join(proj_path, logPath)#拼接文件路径
        log_path = log_path.replace("/","//")
        log_path = log_path.replace("\\","//")
        if os.path.exists(log_path) and os.path.isdir(log_path):#如果没有这个文件夹就新建
            pass
        else:
            mkdirs(log_path)
            
        log_name =os.path.join(log_path,logName)#拼接文件路径
        #print(log_name)
        

        #写入日志文件
        
        #在py3.7出现保存日志文件有中文乱码的情况，需要修改logging文件
        #第1849行，更改为：h = FileHandler(filename, mode,encoding='utf-8')
        
        #按照级别写入: CRITICAL > ERROR > WARNING > INFO > DEBUG
        logging.basicConfig(level=logging.INFO,  #更改level可以控制哪些级别的日志需要写入到日志文件
                format="[%(levelname)s] [%(asctime)s] [pid:%(process)s] [%(filename)s] %(message)s",  
                datefmt="%Y-%m-%d %H:%M:%S",  
                filename=log_name,  
                filemode="a")
        #发送至控制台打印日志信息，注意：控制台打印的日志需要包含在日志文件中
        #按照级别在控制台显示: CRITICAL > ERROR > WARNING > INFO > DEBUG
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  #更改setLevel可以控制在控制台显示哪些级别的日志信息,如这里只有大于等于INOF级别的才会在控制台显示
        #formatter = logging.Formatter("[%(levelname)s] %(message)s")  
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console.setFormatter(formatter)  
        logging.getLogger("").addHandler(console)  
               
  
    def debug(self, msg=""):  
        """ 
        output DEBUG level LOG 
        """  
        logging.debug(str(msg))  
  
    def info(self, msg=""):  
        """ 
        output INFO level LOG 
        """  
        logging.info(str(msg))  
  
    def warning(self, msg=""):  
        """ 
        output WARN level LOG 
        """  
        logging.warning(str(msg))  
  
    def exception(self, msg=""):  
        """ 
        output Exception stack LOG 
        """  
        logging.exception(str(msg))  
  
    def error(self, msg=""):  
        """ 
        output ERROR level LOG 
        """  
        logging.error(str(msg))  
  
    def critical(self, msg=""):  
        """ 
        output FATAL level LOG 
        """  
        logging.critical(str(msg))  
       
def test_Logger():  
    #testlog = Logger(logPath="Log1") #只给一个目录名称
    #testlog = Logger(logName="log1.txt") #只给一个日志文件名称
    testlog = Logger(logPath="Logs/testlog",logName="testlog.txt")#给定一个多级目录名称和文件名称 
    #testlog = Logger() #使用默认目录名和文件名
    testlog.debug(u"这是个debug....")  
    testlog.info("这是个info....")  
    testlog.warning("这是个warning....")  
    testlog.exception("这是个exception....")  
    testlog.error("这是个error....")  
    testlog.critical(u"这是个critical....")  
    try:  
        lists = []  
        print(lists)  
    except Exception:  
        #testlog.error("execute task failed. the error as follows:")  
        testlog.exception("execute task failed. the exception as follows:")  
        exit(1) 


if __name__ == '__main__':
    test_Logger()

