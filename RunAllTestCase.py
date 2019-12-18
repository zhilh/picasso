#-*- coding:utf-8 -*-
'''
Created on 2018年9月26日
@author: zhilh
Description: 自动化测试框架主入口 
'''

from framework.HTMLTestRunner import HTMLTestRunner
from framework.Email import SendEmail
from framework import log
import getcwd

import unittest
import time,os


casepath = os.path.join(getcwd.get_cwd(),"testsuites")  #测试用例存放路径
reportpath = os.path.join(getcwd.get_cwd(),"report")    #测试报告存放路径
reportname = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))+"-result.html" #生成的测试报告文件名

def add_case():
    '''加载测试用例'''
    discover = unittest.defaultTestLoader.discover(casepath,
                                                   pattern="test_*_logout.py",
                                                   top_level_dir=None)
    return discover

def run_case():
    '''执行测试用例，生成测试报告'''   
    htmlreportpath = os.path.join(reportpath,reportname)
    fp = open(htmlreportpath,"wb")
    runner = HTMLTestRunner(stream=fp,
                                           title=u"自动化测试报告",
                                           description=u"测试用例执行情况",
                                           verbosity=2)
    # 调用allcase函数返回值
    runner.run(add_case())
    fp.close()
    log.info('测试报告已生成：'+htmlreportpath)

def sendMail(files):
    mailTitle="曲靖治安平台--测试报告"
    contents="<h1>Hi,<h1><br><h1>你好，这是系统发送的自动化测试报告，请不要回复此邮件<h1><br><h1>详细请查收附件<h1>"
    files=[files]
    mail=SendEmail()
    mail.send_mail(subject=mailTitle, content=contents, files=files)
    

if __name__ == "__main__":
    run_case()
    #sendMail(os.path.join(reportpath,reportname))
    