#-*- coding:utf-8 -*-
'''
Created on 2018年12月7日
@author: zhilh
Description: 人员备案页面元素封装
'''

from framework import rdData

MAIN_IFRAME='id=>main-iframe'  #主窗口

class personIndex(object):
    '''
    人员备案引导页--选择企业类型
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        self.driver=driver
        self.title_name='xpath=>/html/body/div[4]/div/div[1]/h4'  #页面左上角标题
        self.industry_list="xpath=>//div[@class='list-industry-item']"  #行业列表
        self.industry_item="xpath=>/html/body/div[2]/div/div[2]/div[2]/div/ul/li[%d]/div"  #行业列表

    def get_page_title(self):#获取页面标题
        return self.driver.getText(self.title_name)
    
    def select_industry_item(self,val):
        self.driver.click(self.industry_item%val)        
    
    def select_industry(self,val=None):
        self.driver.rightClick(self.industry_list)
        self.driver.waitSleep(1)
        itemN = self.driver.getElements(self.industry_list)
        #print(self.industry_list,itemN)
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)
            #print(items)
            val=rdData.getListItem(items)            
        for i in itemN:
            if i.text.count(val)>0:
                self.driver.waitSleep(1)
                i.click()                

class personInfo(object):
    '''
    人员备案信息填写
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        
        self.driver=driver
        self.title_name='xpath=>/html/body/div[2]/div/div[1]/h4'  #页面左上角标题
        
        #基本信息
        self.person_place='class=>js-set-place-id'#所属场所
        self.person_place_item='class=>autocomplete-suggestion'#场所下拉列表项
        self.person_position='class=>js-set-position-id'#职位/工种
        self.person_position_item='class=>js-set-position-id'#职位/工种下拉列表项
        self.person_country='class=>js-set-country'#国家/地区
        self.person_card='class=>js-set-personal-card'#证件类型
        self.person_id_number='class=>js-set-identification-number'#证件号码
        self.person_name='class=>js-set-name'#姓名
        self.person_birth_date='class=>js-set-birth-date'#出生日期
        self.person_ethnicity='class=>js-set-ethnicity-id'#民族
        self.person_ethnicity_id='class=>js-set-ethnicity-id'#民族下拉列表项
        self.person_address='class=>js-set-permanent-address'#户籍地址
        self.person_issuing_authority='class=>js-set-issuing-authority'#签发机关
        self.person_validity_date_from='class=>js-set-validity-from-date'#有效期-开始
        self.person_validity_date_to='class=>js-set-validity-thru-date'#有效期-结束
        self.person_phone_number='class=>js-set-phone-number'#手机号码
        self.person_current_address='class=>js-set-current-address'#现住详址
        self.person_save_button='class=>js-submit-filings'#提交备案信息按钮
        self.person_success_name='class=>js-modal-success-name'#备案成功后提示框
        self.person_fail_name='class=>js-modal-fail-name'#备案失败后提示框


    ####基本信息#####
    def select_place_position(self,val=None): #所属场所
        self.driver.click(self.person_place)
        self.driver.waitSleep(1)
        itemN = self.driver.getElements(self.person_place_item)
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)
            val=rdData.getListItem(items)
            #print(items,val)
        for i in itemN:
            if i.text.count(val)>0:
                self.driver.waitSleep(1)
                i.click() 
        return val

    def select_person_position(self,val=None): #职位/工种
        self.driver.click(self.person_position)
        self.driver.waitSleep(1)
        itemN = self.driver.getElements(self.person_position)
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text) 
            items=items[0].split('\n')  
            items.remove('--请选择--')
            val=rdData.getListItem(items)
            #print(items,val)
        self.driver.selectByText(self.person_position,val)
        
    def select_person_country(self,val=None): #国家/地区
        itemN = self.driver.getElements(self.person_country)
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)
            items=items[0].split('\n')               
            val=rdData.getListItem(items)
            #print(items,val)
        self.driver.selectByText(self.person_country,val)

    def select_person_card(self,val=None):  #证件类型
        itemN = self.driver.getElements(self.person_card)
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)   
            items=items[0].split('\n')
            val=rdData.getListItem(items)
            #print(items,val)
        self.driver.selectByText(self.person_card,val)

    def input_person_id_number(self,val):  #证件号码
        self.driver.inputText(self.person_id_number,val)
        return val

    def input_person_name(self,val):  #姓名
        self.driver.inputText(self.person_name,val)
        return val

    def input_person_birth_date(self,val):  #出生日期
        self.driver.inputText(self.person_birth_date,val)
        self.driver.click(self.person_name)#点击页面任意一个输入框，消除弹出的日期控件

    def select_person_ethnicity(self,val=None):  #民族
        self.driver.click(self.person_ethnicity)
        itemN = self.driver.getElements(self.person_ethnicity)
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)
            items=items[0].split('\n')
            items.remove('--请选择--')
            val=rdData.getListItem(items)
            #print(items,val)          
        self.driver.selectByText(self.person_ethnicity,val)

    def input_person_address(self,val):  #户籍地址
        self.driver.inputText(self.person_address,val)

    def input_person_issuing_authority(self,val):  #签发机关
        self.driver.inputText(self.person_issuing_authority,val)

    def input_person_validity_date_from(self,val):  #有效期-开始
        self.driver.inputText(self.person_validity_date_from,val)
        self.driver.click(self.person_name)#点击页面任意一个输入框，消除弹出的日期控件

    def input_person_validity_date_to(self,val):  #有效期-结束
        self.driver.inputText(self.person_validity_date_to,val)
        self.driver.click(self.person_name)#点击页面任意一个输入框，消除弹出的日期控件

    def input_person_phone_number(self,val):  #手机号码
        self.driver.inputText(self.person_phone_number,val)
        return val

    def input_person_current_address(self,val):  #现住详址
        self.driver.inputText(self.person_current_address,val)

    def click_person_save_button(self):  #提交备案信息
        self.driver.click(self.person_save_button)

    def person_fail_name_is_enabled(self):#判断备案提交后，失败信息是否可见
        return self.driver.findElement(self.person_fail_name)
    
    def person_success_name_is_enabled(self):#判断备案提交后，成功信息是否可见
        return self.driver.findElement(self.person_success_name)
        
        
        
        

