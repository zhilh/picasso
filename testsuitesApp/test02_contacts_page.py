#-*- coding:utf-8 -*-
'''
Created on 2019年7月11日
@author: zhilh
Description: 联系人页测试
'''

import unittest
from framework.BasesApp import AppDriver
from framework.func import testPass
from framework import log

from pageobjectApp.contacts_page import pageElements 
import warnings


class test_contacts(unittest.TestCase):
    '''联系人页'''
    #测试用例类级的方法，在所有测试用例执行之前执行
    @classmethod
    def setUpClass(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.dr = AppDriver()
        self.page=pageElements(self.dr)
        log.info('测试联系人页功能')
    
    #测试用例类级的方法，在所有测试用例执行完成后执行
    @classmethod
    def tearDownClass(self):
        self.dr.quit()
        log.info('联系人页测试完成')

    def setUp(self):
        print('case_id: ',self.id(),'开始执行<br />') #固定格式，用于报表生成
 
    def tearDown(self):
        '''测试报错或者用例不通过则截图'''
        if not testPass(self):
            print('截图: ',self.dr.getScreenshot( self.id()),'<br />')#固定格式，用于报表生成
        print('结束执行<br />')#固定格式，用于报表生成


    def test_01(self):
        '''联系人页面'''
        self.page.click_contacts_button()
        AR=self.page.find_element_contacts_title()
        self.assertEqual('联系人',AR) 
        
    def test_02(self):
        '''添加好友'''
        self.page.click_add_button()
        AR=self.page.find_element_add_title()
        self.assertEqual('添加好友',AR)
        self.page.click_back_main_button()
        
    def test_03(self):
        '''新的朋友'''
        self.page.click_newfriends_button()
        AR=self.page.find_element_newfriends_title()
        self.assertEqual('新的朋友',AR)
        self.page.click_back_main_button()
        
    def test_04(self):
        '''我的群聊'''
        self.page.click_mychats_button()
        AR=self.page.find_element_chat_name_title()
        self.assertEqual('我的群聊',AR)
        self.page.click_chat_back_button()        

if __name__ == '__main__':
    unittest.main()


    
    