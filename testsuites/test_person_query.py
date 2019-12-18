#-*- coding:utf-8 -*-
'''
Created on 2019年1月18日
@author: zhilh
Description: 从业人员查询
'''

import os
import unittest
from framework.Bases import PySelenium
from framework.login import loginGo
from framework import log
from framework.func import testPass

from pageobject.homepage_menu_page import leftPage
from pageobject.person_query_page import pageElements as centerPage,MAIN_IFRAME

import ddt
from framework.Execl import ExcelUtil
import getcwd



@ddt.ddt
class Industry_Search(unittest.TestCase):
    '''从业人员查询'''
    #装载测试数据
    execlName=os.path.join(getcwd.get_cwd(),"data\\person_query_data.xlsx")
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
        self.menu_page.go_person_query()   #点击菜单到 从业人员查询 功能链接
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
      
        '''从业人员查询'''
        search_dict={
            'place_name':test_data['place_name'].strip(), #所属企业名称
            'industry_name':test_data['industry_name'].strip(), #所属行业
            'region_name':globals()['node_name'].strip(), #所属辖区
            'person_name':test_data['person_name'].strip(), #从业人员姓名
            'person_sex':test_data['person_sex'].strip(), #从业人员性别
            'person_id_card':test_data['person_id_card'].strip(), #从业人员证件号码
            'position_name':test_data['position_name'].strip(), #职位/工种            
            'apply_date_from':test_data['apply_date_from'].strip(), #备案时间-开始            
            'apply_date_to':test_data['apply_date_to'].strip() #备案时间-结束            
            }
        print('查询条件：',search_dict)            
                
        self.page.input_place_name(search_dict['place_name'])#所属企业名称
        self.page.select_industry(search_dict['industry_name'])#所属行业
        #self.page.select_region_name(search_dict['region_name'])#所属辖区
        self.page.input_person_name(search_dict['person_name']) #从业人员姓名
        self.page.select_person_sex(search_dict['person_sex'])#从业人员性别
        self.page.input_person_id_card(search_dict['person_id_card'])#从业人员证件号码
        self.page.input_position_name(search_dict['position_name'])#职位/工种
        self.page.input_apply_date_from(search_dict['apply_date_from']) #备案时间-开始
        self.page.input_apply_date_to(search_dict['apply_date_to'])#备案时间-结束
        self.page.click_search_button()
        self.dr.waitSleep(2)
        
        '''断言：
        1、只验证查询结果第一页数据，只对有查询结果的数据进行准确性验证
        2、根据显示数据，只做部分查询条件验证：所属企业，所属行业，人员姓名，性别，证件号码，职位/工种，备案时间
        3、其他查询条件犹豫没有对应结果显示在页面，暂时无法验证
        4、查询结果中只要有一条数据验证失败，则这条case不通过，只有全部数据验证通过，这条case才通过
        5、这里只验证查询出来的数据是否正确，没有查询到数据的情况无法验证是否正确
        '''
        if search_dict['place_name']=='' and search_dict['industry_name']=='' and search_dict['person_name']==''  \
         and search_dict['person_sex']=='' and search_dict['person_id_card']=='' and search_dict['position_name']=='' \
         and search_dict['apply_date_from']=='' and search_dict['apply_date_to']=='':
            self.assertTrue(1==2,'验证条件（所属企业，所属行业，人员姓名，性别，证件号码，职位/工种，备案时间）为空，不做验证！')        
        table_data=self.page.get_table_data() # 获取查询结果table内的所有数据
        #print(len(table_data),table_data)
        okFlag = -1
        for i in range(len(table_data)):
            #print(search_dict['place_name'],industry_name,': ',table_data[i])
            if int(len(table_data[i])>1):
                okFlag = 0  
                if table_data[i][0].lower().find(search_dict['place_name'].lower()) != -1 and len(search_dict['place_name'])>0:#验证输入了企业名称时，查询结果包含输入的企业名称信息
                    okFlag=1
                if search_dict['industry_name'].lower().find(table_data[i][1].lower()) != -1 and len(search_dict['industry_name'])>0:#验证输入了所属行业时，查询结果包含输入的所属行业信息
                    okFlag=1
                if table_data[i][2].lower().find(search_dict['person_name'].lower()) != -1 and len(search_dict['person_name'])>0:#验证输入了从业人员姓名时，查询结果包含输入的从业人员姓名信息
                    okFlag=1
                if search_dict['person_sex'].lower() == table_data[i][3].lower() and len(search_dict['person_sex'])>0:#验证输入了从业人员性别时，查询结果等于输入的从业人员性别
                    okFlag=1
                if search_dict['person_id_card'].lower() == table_data[i][4].lower() and len(search_dict['person_id_card'])>0:#验证输入了从业人员证件号码时，查询结果等于输入的从业人员证件号码
                    okFlag=1
                if table_data[i][5].lower().find(search_dict['position_name'].lower()) != -1 and len(search_dict['position_name'])>0:#验证输入了职位/工种时，查询结果包含输入的职位/工种信息
                    okFlag=1
                if  table_data[i][7].lower() >= search_dict['apply_date_from'].lower() and len(search_dict['apply_date_from'])>0:#验证输入了备案开始时间时，查询结果》=备案开始时间
                    okFlag=1
                if table_data[i][7].lower() <= search_dict['apply_date_to'].lower()  and len(search_dict['apply_date_to'])>0:#验证输入了备案结束时间时，查询结果《=备案结束时间
                    okFlag=1
                if okFlag == 0:
                    self.assertTrue(1==2,'查询结果验证有错！'+str(table_data[i]))
        if okFlag == -1:
            self.assertTrue(1==2,'查询结果为空，不做验证！')
        else:    
            self.assertTrue(1==1,'首页查询结果验证正确！')
        
        
if __name__ == '__main__':
    unittest.main()


