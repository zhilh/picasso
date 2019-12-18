#-*- coding:utf-8 -*-
'''
Created on 2019年7月8日
@author: zhilh
Description: 通用app登录功能测试
'''

import unittest
from framework.BasesApp import AppDriver
from framework.func import testPass
from framework import log
import getcwd

from pageobjectApp.login_page import pageElements 
import os

import ddt
from framework.Execl import ExcelUtil
import warnings



@ddt.ddt
class test_login(unittest.TestCase):
    '''登录页'''
    #装载测试数据
    execlName=os.path.join(getcwd.get_cwd(),"data\\YDJFN_login_account_app.xlsx")
    caseData_excel = ExcelUtil(execlName, 'Sheet1')
    log.info('装载测试数据成功')
    
    #测试用例类级的方法，在所有测试用例执行之前执行
    @classmethod
    def setUpClass(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.dr = AppDriver()
        self.page=pageElements(self.dr)
        log.info('测试App登录功能')
    
    #测试用例类级的方法，在所有测试用例执行完成后执行
    @classmethod
    def tearDownClass(self):
        self.dr.quit()
        log.info('登录功能测试完成')

    def setUp(self):
        print('case_id: ',self.id(),'开始执行<br />') #固定格式，用于报表生成
 
    def tearDown(self):
        '''测试报错或者用例不通过则截图'''
        if not testPass(self):
            print('截图: ',self.dr.getScreenshot( self.id()),'<br />')#固定格式，用于报表生成
        print('结束执行<br />')#固定格式，用于报表生成

    @ddt.data(*caseData_excel.next()) 
    def test_login(self,test_data):
        '''测试登录功能'''
        login_name=test_data['login_name'] #登录账号
        password=test_data['password'] #密码
        ER=test_data['ER'] #预期结果
        desc=test_data['desc'] #测试描述
        AR=''#实际结果
        print('测试用例描述：%s' %(desc))
        print('账号：%s' %(login_name))
        print('密码：%s' %(password))

        self.page.input_login_name(login_name)
        self.page.input_password(password)
        self.page.click_login_button()
        if self.page.find_element():
            AR='登录成功'
        else:
            AR='登录失败'
        print(AR)
        self.assertEqual(ER,AR) 
        

if __name__ == '__main__':
    unittest.main()


    
    