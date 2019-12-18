#-*- coding:utf-8 -*-
'''
Created on 2018年11月13日
@author: zhilh
Description: 企业备案
'''

import unittest,os
from framework.Bases import PySelenium
from framework.login import loginGo
from framework import log
from framework.func import testPass
from framework import rdData

from pageobject.homepage_menu_page import leftPage
from pageobject.place_filing_page import placeIndex,placeBasicInfo,placeExtras,placeDevices,MAIN_IFRAME
import ddt
from framework.Execl import ExcelUtil,ExcelAdd
import getcwd


@ddt.ddt
class place_filing(unittest.TestCase):
    '''企业备案'''
    #装载测试数据
    execlName=os.path.join(getcwd.get_cwd(),"data\\place_filing_data.xls")
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
        self.menu_page.go_add_place()   #点击左边菜单的 新增企业备案
        self.dr.switchFrame(MAIN_IFRAME)   #指向iframe页，中间数据展示位置
             
    def tearDown(self):
        '''测试报错或者用例不通过则截图'''
        if not testPass(self):
            print('截图: ',self.dr.getScreenshot( self.id()),'<br />')#固定格式，用于报表生成
        print('结束执行<br />')#固定格式，用于报表生成
        self.dr.switchFrameOut()    #指向iframe上一级，左边菜单位置

    @ddt.data(*caseData_excel.next())  
    def test_index(self,test_data):
     
        place_dict={
            'cur_row':test_data['curRow'],#当前execl数据表数据行
            'place_name':test_data['place_name'].strip(), #企业名称
            'industry_name':test_data['industry_name'].strip(), #所属行业
            'person_name':test_data['person_name'].strip(), #法人姓名
            'person_phone':test_data['person_phone'].strip(), #法人电话号码           
            }
        print('备案信息：',place_dict)            
        
        
        '''第一页 选择行业'''
        self.page=placeIndex(self.dr) #企业备案引导首页 元素
        self.assertEqual('新增企业备案' ,self.page.get_page_title(),'页面标题不一致')
        self.page.select_industry(place_dict['industry_name'])
         

        '''第二页 输入基本信息'''
        self.page=placeBasicInfo(self.dr)
        #单位基本信息
        self.dr.waitSleep(1)
        self.dr.mouseScroll(1000)#滚动鼠标,消除鼠标右键菜单
        self.page.input_place_name(place_dict['place_name'])#输入单位名称
        self.page.input_business_address('成都市人民北路'+str(rdData.getInt(2))+'号')#定位单位经营地址
        self.page.select_has_certificate('有') #有无证照
        self.page.input_opening_date(rdData.getDate()) #开业日期
        self.page.input_fax(rdData.getInt(6)) #单位传真
        self.page.input_web_address(rdData.getGBK2312(15)) #单位网址
        self.page.input_phone_number(rdData.getPhone()) #单位电话
        self.page.select_operating_state('营业') #经营状态
        
        #营业执照信息
        self.dr.waitSleep(1)
        self.page.input_uniform_social_credit_code(rdData.getInt(10))#统一社会信用代码/注册号
        self.page.input_organization_code(rdData.getInt(6))#组织机构代码
        self.page.input_company_name(rdData.getGBK2312(6)) #营业执照企业名称
        self.page.input_company_english_name(rdData.getStrings())#单位英文名称
        self.page.select_company_type()#单位性质
        self.page.input_registered_address(rdData.getGBK2312(3))#单位注册地址
        self.page.input_issue_date(rdData.getDate())#发照日期
        self.page.input_registered_capital(str(rdData.getInt(3))+'万')##注册资本
        self.page.input_establishment_date(rdData.getDate())##成立日期
        self.page.input_business_from(rdData.getDate())##经营期限-开始
        self.page.input_business_to(rdData.getDate(2000,3000))#经营期限-结束
        self.page.input_business_scope(rdData.getGBK2312(4))#经营范围
        
        #弹框页面，输入人员信息        
        self.dr.waitSleep(1)
        self.page.click_add_practitioner()#点击添加人员按钮
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
        self.page.input_person_current_address(rdData.getGBK2312(30))#现住详址
        self.page.click_person_save_button()#点击保存人员按钮
        
        #管辖信息
        self.dr.mouseScroll(-1000)#滚动鼠标，到页面底部
        self.dr.waitSleep(1)
        self.page.select_region(globals()['node_name'])#管辖机构
        self.page.input_region_police(globals()['login_name'])#责任民警,从管辖机构中带出
        self.page.input_region_phone(rdData.getPhone())#机构办公电话
        self.page.click_second_step()#点击下一步按钮

       
        '''第三页 输入附加信息'''
        self.page=placeExtras(self.dr)
        self.dr.mouseScroll(1000)#滚动鼠标，到页面顶部
        #self.dr.js('window.scrollTo(0,document.body.scrollHeight)')
        self.dr.waitSleep(1)
        
        if place_dict['industry_name']== '保安服务业' :
            self.page.input_special_number()
            self.page.input_special_issuing_authority()
            self.page.input_special_issuing_date()
            self.page.click_special_licence_always_valid()
            
        if place_dict['industry_name']== '危化业' :
            self.page.select_chemistry_place_type()    #单位类型
            self.page.select_chemistry_involve_type()    #涉及环节
            self.page.select_danger_level()  #存放危险等级
            self.page.input_weihua_office_phone_number(rdData.getPhone())   #值班室电话
            self.page.input_weihua_monitor_phone_number(rdData.getPhone())   #监控室电话
            #self.page.input_product_name()#危化产品
            #self.page.click_product_add_btn()#点击添加危化品按钮
            self.dr.mouseScroll(-1000)#滚动鼠标，到页面底部
            self.page.input_warehouse_name(rdData.getGBK2312(6))#仓库名称
            self.page.input_warehouse_address('成都市人民北路'+str(rdData.getInt(2))+'号')#仓库地址
            #self.page.upload_warehouse_img('D:\Python\eclipse-workspace\picasso\img\jslogo.png')#上传仓库平面图
            self.page.input_warehouse_IMEI('0869976033706103')#仓库IMEI
            #self.page.click_warehouse_add_btn() #点击添加仓库
                        
        if place_dict['industry_name']== '娱乐业' :
            self.page.input_fire_safety_responsibility_number()
            self.page.input_hygienic_license_number()
            self.page.input_housing_safety_approval_number()
            self.page.input_environmental_department_document()
            self.page.input_yule_business_area()
            self.page.input_yule_balcony_count()
            self.page.input_safety_equipment()
            self.page.input_fire_fighting_device()
            
        if place_dict['industry_name']== '旅馆业' :
            self.page.input_hotel_building_area()  #建筑总面积       
            self.page.input_hotel_business_area()  #营业面积       
            self.page.input_hotel_balcony_area()  #包厢面积       
            self.page.input_hotel_building_count()  #楼栋数      
            self.page.input_hotel_floor_count()  #楼层数       
            self.page.input_hotel_room_count()  #房间总数       
            self.page.input_hotel_bed_count()  #核定内容       
            self.page.input_hotel_gateway_count() #出入口 
            self.page.input_hotel_selling_area()  #营业厅
            self.page.input_hotel_passageway_count()  #通道
            self.page.input_hotel_storehouse_count()   #保管库房
            self.page.input_hotel_parking_lot()  #停车场
            self.page.input_hotel_other_part()  #其他部位
        
        self.page.click_third_step()    #点击下一步按钮
              
        '''第四页 输入设备信息'''
        self.page=placeDevices(self.dr)
        self.dr.waitSleep(1)
        self.page.input_device_name(rdData.getGBK2312(10))    #设备名称
        self.page.input_device_count(rdData.getInt(1))    #设备数量
        #self.page.click_save_button() #点击保存功能按钮
        if self.page.place_success_name_is_enabled():
            self.assertTrue(1==1,'企业备案成功')
            self.writer_table.modify_cell(place_dict['cur_row'], 5,globals()['node_name'])
            self.writer_table.modify_cell(place_dict['cur_row'], 6,'备案成功')
            log.info("企业备案成功:%s,%s,%s,%s" %(globals()['node_name'],globals()['login_name'],place_dict['industry_name'],place_dict['place_name']))
        else:
            self.assertTrue(1==2,'企业备案失败')
        
        
if __name__ == '__main__':
    unittest.main()



