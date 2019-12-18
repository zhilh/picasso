#-*- coding:utf-8 -*-
'''
Created on 2019年2月1日
@author: zhilh
Description: 企业注销
'''

import os
import unittest
from framework.Bases import PySelenium
from framework.login import loginGo
from framework import log
from framework.func import testPass

from pageobject.homepage_menu_page import leftPage
from pageobject.place_logout_page import pageElements as centerPage,MAIN_IFRAME

import ddt
from framework.Execl import ExcelUtil
import getcwd



@ddt.ddt
class Industry_Search(unittest.TestCase):
    '''企业注销'''
    #装载测试数据
    execlName=os.path.join(getcwd.get_cwd(),"data\\place_logout_data.xlsx")
    caseData_excel = ExcelUtil(execlName, 'Sheet1')
    log.info('装载测试数据成功')

    @classmethod
    def setUpClass(self):
        self.dr = PySelenium()
        loginGo(self.dr).click_login()#登录系统
        self.menu_page=leftPage(self.dr) #左边菜单元素
        globals()['login_name']=self.menu_page.get_login_name()  #登录用户名
        globals()['node_name']=self.menu_page.get_node_name()    #登录用户所属机构名
        log.info('登录系统成功，开始测试...')
    
    @classmethod
    def tearDownClass(self):
        #self.page.set_iframe_out()    #指向iframe上一级，左边菜单位置
        #self.menu_page.go_login_out()  #退出登录
        self.dr.quit()  #关闭浏览器
        log.info('测试完成，退出系统，关闭浏览器')
    
    def setUp(self):        
        print('case_id: ',self.id(),'开始执行<br />') #固定格式，用于报表生成
        self.menu_page.go_place_logout()   #点击菜单到 企业注销 功能链接
        self.dr.switchFrame(MAIN_IFRAME)   #指向iframe页，中间数据展示位置
               
    def tearDown(self):
        '''测试报错或者用例不通过则截图'''
        if not testPass(self):
            print('截图: ',self.dr.getScreenshot( self.id()),'<br />')#固定格式，用于报表生成
        print('结束执行<br />')#固定格式，用于报表生成
        self.dr.switchFrameOut()    #指向iframe上一级，左边菜单位置
  
    
    @ddt.data(*caseData_excel.next())  
    def test_index(self,test_data):
        self.page=centerPage(self.dr)
      
        '''企业查询'''
        search_dict={
            'place_name':test_data['place_name'].strip(), #企业名称
            'industry_name':test_data['industry_name'].strip(), #所属行业
            'region_name':test_data['region_name'].strip(), #管辖机构
            'place_code':test_data['place_name'].strip(),#统一社会信用代码/注册号
            #'region_police':test_data['region_police'].strip(), #责任民警
            'person_name':test_data['person_name'].strip(), #法人姓名
            #'person_id_card':test_data['person_id_card'].strip(), #法人证件号码
            'place_type':test_data['place_type'].strip(), #企业类型            
            'operating_state':test_data['operating_state'].strip(), #营业状态
            #'opening_date_from':test_data['opening_date_from'].strip(), #开业时间-开始            
            #'opening_date_to':test_data['opening_date_to'].strip() #开业时间-结束            
            }
        print('查询条件：',search_dict)            
                
        self.page.input_place_name(search_dict['place_name'])#输入企业名称
        self.page.select_industry(search_dict['industry_name'])#所属行业
        if search_dict['region_name']!='':
            self.page.select_region_first_name(search_dict['region_name'])#管辖机构
        #self.page.input_region_police(search_dict['region_police']) #责任民警/编号
        self.page.input_person_name(search_dict['person_name'])#法人姓名
        #self.page.input_person_id_card(search_dict['person_id_card'])#法人身份证
        self.page.select_input_place_type(search_dict['place_type'])#企业类型
        self.page.select_operating_state(search_dict['operating_state'])#经营状态
        #self.page.input_opening_date_from(search_dict['opening_date_from']) #开业时间-开始
        #self.page.input_opening_date_to(search_dict['opening_date_to'])#开业时间-结束
        self.page.click_search_button()
        self.dr.waitSleep(2)
        
        '''断言查询结果：
        1、只验证查询结果第一页数据，只对有查询结果的数据进行准确性验证
        2、根据显示数据，只做部分查询条件验证： 场所名称、所属行业、企业法人、企业类型、经营状态、统一社会信用代码/注册号
        3、其他查询条件犹豫没有对应结果显示在页面，暂时无法验证
        4、查询结果中只要有一条数据验证失败，则这条case不通过，只有全部数据验证通过，这条case才通过
        5、这里只验证查询出来的数据是否正确，没有查询到数据的情况无法验证是否正确
        '''
        if search_dict['place_name']=='' and search_dict['industry_name']=='' and search_dict['person_name']==''  \
        and search_dict['place_type']=='所有' and search_dict['region_name']=='' and search_dict['operating_state']=='所有'  \
        and search_dict['place_code']==''  :
            self.assertTrue(1==2,'查询条件（场所名称、所属行业、企业法人、企业类型、管辖机构、经营状态、统一社会信用代码/注册号）为空，不做注销操作！')        
        table_data=self.page.get_table_data() # 获取查询结果table内的所有数据
        #print(len(table_data),table_data)
        okFlag = -1
        for i in range(len(table_data)):
            #print(search_dict['place_name'],industry_name,': ',table_data[i])
            if int(len(table_data[i])>1):
                okFlag = 0  
                if (table_data[i][0].lower().find(search_dict['place_name'].lower()) != -1 and len(search_dict['place_name']) >0) \
                or ( table_data[i][7].lower() == search_dict['place_code'].lower() and search_dict['place_code']!=''):#验证输入了企业名称时，查询结果企业名称（或者统一社会信用代码/注册号）包含输入的企业名称信息
                    okFlag=1
                if search_dict['industry_name'].lower().find(table_data[i][1].lower()) != -1 and len(search_dict['industry_name'])>0:#验证输入了所属行业时，查询结果包含输入的所属行业信息
                    okFlag=1
                if table_data[i][2].lower().find(search_dict['person_name'].lower()) != -1 and len(search_dict['person_name'])>0:#验证输入了企业法人时，查询结果包含输入的企业法人信息
                    okFlag=1
                if search_dict['place_type']==table_data[i][3] and search_dict['place_type']!='所有' :#验证输入了企业类型时，查询结果等于输入的企业类型信息
                    okFlag=1
                if search_dict['operating_state'] == table_data[i][3] and search_dict['operating_state']!='所有' :#验证输入了经营状态时，查询结果等于输入的经营状态信息
                    okFlag=1
                if table_data[i][7].lower().find(search_dict['region_name'].lower()) != -1 and search_dict['region_name']!='':#验证输入了管辖机构时，查询结果包含输入的管辖机构信息，不包含该管辖机构的下属机构
                    okFlag=1
                if okFlag == 0:
                    self.assertTrue(1==2,'查询结果验证有错！'+str(table_data[i]))
        if okFlag == -1:
            self.assertTrue(1==2,'查询结果为空，不做注销操作！')
        
        #注销，只注销列表的第一条数据
        for i in range(len(table_data)):
            if int(len(table_data[i])>1 ):
                self.page.select_logout_button(i)#选择点击注销按钮
                self.page.input_contents('Auto logout by automated tester')#选择点击注销按钮
                self.page.select_logout_type()#注销类型
                #self.page.click_confirm_button()#点击注销确认按钮
                if self.page.logout_success_name_is_enabled():
                    self.assertTrue(1==1,'企业注销成功')
                    log.info("企业注销成功，操作员：%s，%s；注销信息：%s，%s，%s，%s" %(globals()['node_name'],globals()['login_name'],table_data[i][0],table_data[i][2],table_data[i][3],table_data[i][4]))
                else:
                    self.assertTrue(1==2,"企业注销失败：%s"%self.page.get_fail_text())
                break
        
if __name__ == '__main__':
    unittest.main()


