#-*- coding:utf-8 -*-
'''
Created on 2018年12月7日
@author: zhilh
Description: 人员备案
'''



import unittest,os
from framework.Bases import PySelenium
from framework.login import loginGo
from framework import log
from framework.func import testPass
from framework import rdData

from pageobject.homepage_menu_page import leftPage
from pageobject.person_filing_page import personIndex,personInfo,MAIN_IFRAME
import ddt
from framework.Execl import ExcelUtil,ExcelAdd
import getcwd


@ddt.ddt
class place_filing(unittest.TestCase):
    '''人员备案'''
    #装载测试数据
    execlName=os.path.join(getcwd.get_cwd(),"data\\person_filing_data.xls")
    caseData_excel = ExcelUtil(execlName, 'Sheet1')
    writer_table=ExcelAdd(execlName,sheet='Sheet1')
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
        self.writer_table.save()#保存测试结果
        #self.dr.quit()  #关闭浏览器
        log.info('测试完成，退出系统，关闭浏览器')
    
    def setUp(self):
        print('case_id: ',self.id(),'开始执行<br />') #固定格式，用于报表生成        
        self.menu_page.go_add_person()   #点击左边菜单的 新增企业备案
        self.dr.switchFrame(MAIN_IFRAME)   #指向iframe页，中间数据展示位置
              
    def tearDown(self):
        '''测试报错或者用例不通过则截图'''
        if not testPass(self):
            print('截图: ',self.dr.getScreenshot( self.id()),'<br />')#固定格式，用于报表生成
        print('结束执行<br />')#固定格式，用于报表生成
        self.dr.switchFrameOut()    #指向iframe上一级，左边菜单位置


         
    @ddt.data(*caseData_excel.next())
    def test_index(self,test_data):
        '''读取从业人员信息'''
        place_dict={
            'cur_row':test_data['curRow'],#当前execl数据表数据行
            'place_name':test_data['place_name'].strip(), #企业名称
            'industry_name':test_data['industry_name'].strip(), #所属行业
            'person_name':test_data['person_name'].strip(), #姓名
            'person_phone':test_data['person_phone'].strip(), #电话号码           
            }
        print('备案信息：',place_dict)            

        '''选择行业'''
        self.page=personIndex(self.dr) #企业备案引导首页 元素
        self.assertEqual('新增从业人员备案' ,self.page.get_page_title(),'页面标题不一致')
        self.page.select_industry(place_dict['industry_name'])

        '''输入人员基本信息'''
        self.page=personInfo(self.dr)
        self.dr.waitSleep(1)
        self.dr.mouseScroll(1000)#滚动鼠标到顶部
        place_position = self.page.select_place_position()#所属场所
        self.page.select_person_position()#职位/工种
        self.page.select_person_country()#国家/地区
        self.page.select_person_card()#证件类型
        self.page.input_person_id_number(rdData.getIdNumber(1)[0])#证件号码
        self.page.input_person_name(place_dict['person_name'])#姓名
        self.page.input_person_birth_date(rdData.getDate(-10000,-9000))#出生日期
        self.page.select_person_ethnicity()#民族
        self.page.input_person_address(rdData.getGBK2312(20))#户籍地址
        self.page.input_person_issuing_authority(rdData.getGBK2312(10))#签发机关
        self.page.input_person_validity_date_from(rdData.getDate(0, 30))##有效期-开始
        self.page.input_person_validity_date_to(rdData.getDate(1000,3000))#有效期-结束
        self.page.input_person_phone_number(place_dict['person_phone'])#手机号码
        #phone_number = self.page.input_person_phone_number('1355034796+')#手机号码
        self.page.input_person_current_address(rdData.getGBK2312(30))#现住详址
        
        self.dr.mouseScroll(-1000)#滚动鼠标到底部
        #self.page.click_person_save_button()#点击保存人员按钮
        if self.page.person_success_name_is_enabled():
            self.assertTrue(1==1,'人员备案成功')
            self.writer_table.modify_cell(place_dict['cur_row'], 5,globals()['node_name'])
            self.writer_table.modify_cell(place_dict['cur_row'], 6,'备案成功')
            log.info("人员备案成功:%s,%s,%s,%s,%s" %(place_position,place_dict['person_name'],place_dict['person_phone'],globals()['node_name'],globals()['login_name']))
        else:
            self.assertTrue(1==2,'人员备案失败')

        
if __name__ == '__main__':
    unittest.main()
