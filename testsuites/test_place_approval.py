#-*- coding:utf-8 -*-
'''
Created on 2019年1月10日
@author: zhilh
Description: 企业备案审核
'''

import unittest
from framework.Bases import PySelenium
from framework.login import loginGo
from framework import log
from framework.func import testPass
from framework import rdData

from pageobject.homepage_menu_page import leftPage
from pageobject.place_approval_page import placeHome,placeApprove,MAIN_IFRAME

class place_approve(unittest.TestCase):
    '''企业备案 审核'''
    @classmethod
    def setUpClass(self):
        self.dr = PySelenium()
        loginGo(self.dr).click_login()#登录系统
        log.info('登录系统成功，开始测试...')
    
    @classmethod
    def tearDownClass(self):
        #self.dr.quit()  #关闭浏览器
        log.info('测试完成，退出系统，关闭浏览器')
    
    def setUp(self):        
        print('case_id: ',self.id(),'开始执行<br />') #固定格式，用于报表生成        
              
    def tearDown(self):
        '''测试报错或者用例不通过则截图'''
        if not testPass(self):
            print('截图: ',self.dr.getScreenshot( self.id()),'<br />')#固定格式，用于报表生成
        print('结束执行<br />')#固定格式，用于报表生成


    @unittest.Myskip
    def test_01_select_function(self):
        '''选择左边菜单功能'''
        self.page=leftPage(self.dr) #左边菜单元素
        self.assertEqual('行业信息概览' ,self.page.get_page_title(),'页面标题不一致')
        self.page.go_approve_place()   #点击左边菜单的 人员审核
        globals()['login_name']=self.page.get_login_name()  #登录用户名
        globals()['node_name']=self.page.get_node_name()    #登录用户所属机构名
        self.dr.switchFrame(MAIN_IFRAME)   #指向iframe页，中间数据展示位置
        
    @unittest.skip('不执行退出功能')
    def test_99_exit(self):
        '''点击退出功能'''       
        self.dr.switchFrameOut()    #指向iframe上一级，左边菜单位置
        self.page=leftPage(self.dr) #左边菜单元素
        self.page.go_login_out()  #退出登录
        self.assertIn('登录' ,self.page.get_page_title(),'页面标题不一致')
                
    @unittest.Myskip
    def test_02_select_place(self):
        '''选择待审核企业列表中的第一条数据进行审核'''
        self.page=placeHome(self.dr) #企业备案引导首页 元素
        self.assertEqual('企业备案审核' ,self.page.get_page_title(),'页面标题不一致')
        self.dr.waitSleep(2)
        table_data=self.page.get_table_data() # 获取查询结果table内的所有数据
        if int(len(table_data))<2:
            self.assertTrue(1==2,'企业备案审核未执行，没有发现待审核企业备案')
        for i in range(len(table_data)):
            if int(len(table_data[i])>1 ):
                place_name=table_data[i][2]
                approve_type=table_data[i][5]
                self.page.select_approve_button(i)
                break                
        
        '''填写审核信息'''    
        self.dr.waitSleep(1)    
        self.pageAp=placeApprove(self.dr)#审核信息填写页面
        self.assertEqual('审核' ,self.pageAp.get_page_title(),'页面标题不一致')
        self.pageAp.select_approve_pass()   #选择审核通过
        self.pageAp.select_approve_finish() #选择审核完成
        #self.pageAp.select_approve_result('通过')
        #self.pageAp.select_processing_mode('审核完成')
        self.pageAp.input_approve_comments(rdData.getGBK2312(30)) #输入审核意见
        self.pageAp.click_approve_button()  #点击审核确认按钮   
        if self.pageAp.approve_success_name_is_enabled():
            self.assertTrue(1==1,'企业备案审核成功')
            log.info("企业备案审核成功，操作员：%s，%s；审核信息：%s，%s" %(globals()['node_name'],globals()['login_name'],place_name,approve_type))
        else:
            self.assertTrue(1==2,"企业备案审核失败：%s"%self.pageAp.get_fail_text())

        
if __name__ == '__main__':
    unittest.main()


