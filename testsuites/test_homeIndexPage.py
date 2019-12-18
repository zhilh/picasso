#-*- coding:utf-8 -*-
'''

Created on 2018年9月17日

@author: zhilh

'''
import unittest
from framework.Bases import PySelenium
from framework.login import loginGo
from framework.func import testPass
from framework import log
from pageobject.homepage_menu_page import leftPage


class test_index(unittest.TestCase):
    '''首页左边菜单功能验证'''
    @classmethod
    def setUpClass(self):
        self.dr = PySelenium()
        self.page=leftPage(self.dr)
        log.info('测试主页菜单链接功能')
    
    @classmethod
    def tearDownClass(self):
        self.dr.quit()
        log.info('主页菜单链接功能测试完成')
    
    def setUp(self):
        print('case_id: ',self.id(),'开始执行<br />') #固定格式，用于报表生成
       
    def tearDown(self):
        '''测试报错或者用例不通过则截图'''
        if not testPass(self):
            print('截图: ',self.dr.getScreenshot( self.id()),'<br />')#固定格式，用于报表生成
        print('结束执行<br />')#固定格式，用于报表生成
             
    
    def test_01_login(self):
        '''登录系统'''
        loginGo(self.dr).click_login()
        self.assertEqual('行业信息概览' ,self.page.get_page_title(),'登录失败')

    @unittest.Myskip
    def test_998_option_link(self):
        '''测试修改密码链接功能'''
        self.page.go_modify_password()
        self.assertEqual('修改密码' ,self.page.get_page_title(),'页面标题不一致')
     
    @unittest.Myskip
    def test_999_option_link(self):
        '''测试退出系统功能'''
        self.page.go_login_out()
        self.assertIn('登录' ,self.page.get_page_title(),'退出系统失败')

    @unittest.Myskip
    def test_02_option_link(self):
        '''测试行业查询链接功能'''
        self.page.go_HYCX()
        self.assertEqual('行业查询' ,self.page.get_page_title(),'页面标题不一致')
 
    @unittest.Myskip
    def test_03_option_link(self):
        '''测试紧急情况保安调动链接功能'''
        self.page.go_JJQKBADD()
        self.dr.waitSleep(2)
        self.assertEqual('紧急情况保安调动' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip 
    def test_04_option_link(self):
        '''测试警保联动历史记录链接功能'''
        self.page.go_JBLDLSJL()
        self.assertEqual('警保联动历史记录' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_05_option_link(self):
        '''测试保安行业统计链接功能'''
        self.page.go_BAHYTJ()
        self.assertEqual('保安行业统计' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_06_option_link(self):
        '''测试单位新增链接功能'''
        self.page.go_DWXZ()
        self.assertEqual('新增单位备案' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_07_option_link(self):
        '''测试单位修改链接功能'''
        self.page.go_DWXG()
        self.assertEqual('单位备案变更' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_08_option_link(self):
        '''测试单位注销链接功能'''
        self.page.go_DWZX()
        self.assertEqual('单位备案注销' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_09_option_link(self):
        '''测试人员查询链接功能'''
        self.page.go_RYCX()
        self.assertEqual('人员查询' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_10_option_link(self):
        '''测试人员新增链接功能'''
        self.page.go_RYXZ()
        self.assertEqual('人员新增' ,self.page.get_page_title(),'页面标题不一致')
  
    @unittest.Myskip
    def test_11_option_link(self):
        '''测试人员修改链接功能'''
        self.page.go_RYXG()
        self.assertEqual('人员修改' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_12_option_link(self):
        '''测试人员注销链接功能'''
        self.page.go_RYZX()
        self.assertEqual('人员注销' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_13_option_link(self):
        '''测试单位检查链接功能'''
        self.page.go_DWJC()
        self.assertEqual('单位检查' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_14_option_link(self):
        '''测试单位检查统计链接功能'''
        self.page.go_JCTJ()
        self.assertEqual('单位检查统计' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_15_option_link(self):
        '''测试全警情报检索链接功能'''
        self.page.go_QJQBJS()
        self.assertEqual('全警情报检索' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_16_option_link(self):
        '''测试报警查询链接功能'''
        self.page.go_BJCX()
        self.assertEqual('报警查询' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_17_option_link(self):
        '''测试场所视频监控链接功能'''
        self.page.go_CSSPJK()
        self.assertEqual('场所视频监控' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_18_option_link(self):
        '''测试场所视频回放链接功能'''
        self.page.go_CSSPHF()
        self.assertEqual('场所视频回放' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_19_option_link(self):
        '''测试消息发布链接功能'''
        self.page.go_XXFB()
        self.assertEqual('消息发布' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_20_option_link(self):
        '''测试发布历史查询链接功能'''
        self.page.go_FBLSCX()
        self.assertEqual('信息发布历史查询' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_21_option_link(self):
        '''测试机构管理链接功能'''
        self.page.go_JGGL()
        self.assertEqual('机构管理' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_22_option_link(self):
        '''测试用户管理链接功能'''
        self.page.go_YHGL()
        self.assertEqual('用户管理' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_23_option_link(self):
        '''测试用户组管理链接功能'''
        self.page.go_YHZGL()
        self.assertEqual('用户组管理' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_24_option_link(self):
        '''测试用户分组管理链接功能'''
        self.page.go_YHFZGL()
        self.assertEqual('用户分组管理' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_25_option_link(self):
        '''测试打分表设置链接功能'''
        self.page.go_DFBSZ()
        self.assertEqual('打分表管理' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_26_option_link(self):
        '''测试数据字典链接功能'''
        self.page.go_SJZD()
        self.assertEqual('数据字典' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_27_option_link(self):
        '''测试参数设置链接功能'''
        self.page.go_CSSZ()
        self.assertEqual('参数设置' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_28_option_link(self):
        '''测试扩展数据字段链接功能'''
        self.page.go_KZSJZD()
        self.assertEqual('扩展数据字段' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_29_option_link(self):
        '''测试工作日志链接功能'''
        self.page.go_workLog()
        self.assertEqual('工作日志' ,self.page.get_page_title(),'页面标题不一致')

    @unittest.Myskip
    def test_30_option_link(self):
        '''测试操作日志链接功能'''
        self.page.go_operationLog()
        self.assertEqual('操作日志' ,self.page.get_page_title(),'页面标题不一致')

        
       
if __name__ == '__main__':
    unittest.main()

    
    