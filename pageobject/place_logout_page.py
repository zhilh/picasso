#-*- coding:utf-8 -*-
'''
Created on 2019年2月1日
@author: zhilh
Description: 企业注销页面封装
'''
from framework import rdData



MAIN_IFRAME='id=>main-iframe'  #主窗口

class pageElements(object):
    '''
    企业注销页面元素
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        self.driver=driver
        self.main_iframe='id=>main-iframe'  #主窗口
        self.title_name='class=>panel-heading'  #首页标题
        
        self.place_name='class=>js-name'  #企业名称
        
        self.select_industry_btn='class=>bs-placeholder' #选择所属行业按钮
        self.industrys='class=>text'#所属行业列表
        self.region='class=>region-value-area'  #管辖机构
        self.region_first='id=>ztreeid0_1_span'  #管辖机构-第一个，可能为空
        self.region_input='class=>region-search-tree-box'  #机构名称输入框
        self.select_all='class=>select-all-tree-btn'  #全选
        self.select_clear='class=>quit-select-all-tree-btn'   #清除
        self.region_search='class=>tree-search-btn'   #管辖机构查询按钮        
        self.region_police='class=>js-police'#责任民警
        self.region_police_select='class=>autocomplete-suggestion'    #下拉选项候选民警

        self.person_name='class=>js-legal-person-name'  #法人姓名
        self.person_id_card='class=>js-legal-person-identification-number'  #法人身份证号
        self.place_type='class=>js-type'  #企业类型
        self.operating_state='class=>js-operating-state'   #经营状态
        self.opening_date_from='class=>js-opening-date-from'   #开业时间-开始
        self.opening_date_to='class=>js-opening-date-to'   #开业时间-结束
        self.search_button='class=>js-search'  #确认查询
                
        self.rows='class=>text-primary'#查询结果显示条数
        self.rt_table='table-striped'#存放查询结果的表格
        self.logout_button='xpath=>//*[@class="js-dereistrations-tbody"]/tr[%d]/td[10]/a'#注销按钮，每条数据的注销按钮定位根据tr值
        
        #注销弹框
        self.logou_type =  'class=>js-set-type'#注销类型
        self.contents='class=>js-set-reason'#注销原因
        self.confirm_button='class=>js-submit-button'  #确认注销
        self.logout_success_name='xpath=>//*[@id="modal-success"]/div/div/div/p[1]'#审核成功后提示框
        self.logout_fail_name='xpath=>//*[@id="modal-fail"]/div/div/div/p[1]'#审核失败后提示框
        
    
    def get_title_name(self):   #获取页面标题
        self.driver.getText(self.title_name)
        
    def input_place_name(self,val):   #输入企业名称
        self.driver.inputText(self.place_name,val)

    def select_industry(self,val):   #所属行业
        self.driver.click(self.select_industry_btn)
        elet_list = self.driver.getElements(self.industrys) 
        if val == None or val.strip()=='':
            val='[]'
        vals=eval(val)
        for i in range(len(elet_list)):
            for j in vals:
                #print(elet_list[i].text,j)
                if elet_list[i].text==j:
                    elet_list[i].click()

    def select_region_name(self,val):  #管辖机构,包含下属机构
        self.driver.click(self.region)
        self.driver.click(self.select_clear)
        self.driver.inputText(self.region_input,val)
        self.driver.click(self.region_search)
        self.driver.click(self.select_all)
        
    def select_region_first_name(self,val):  #管辖机构,只选择第一个机构
        self.driver.click(self.region)
        self.driver.click(self.select_clear)
        self.driver.inputText(self.region_input,val)
        self.driver.click(self.region_search)
        if self.driver.findElement(self.region_first,2):
            self.driver.click(self.region_first)
        
    def input_region_police(self,val):   #责任民警/编号
        self.driver.inputText(self.region_police,val)
        
    def input_person_name(self,val):   #法人姓名
        self.driver.inputText(self.person_name,val)
        
    def input_person_id_card(self,val):   #法人身份证
        self.driver.inputText(self.person_id_card,val)
        
    def select_input_place_type(self,val):   #企业类型
        self.driver.selectByText(self.place_type,val)
        
    def select_operating_state(self,val):   #经营状态
        self.driver.selectByText(self.operating_state,val)
        
    def input_opening_date_from(self,val):   #开业时间-开始
        self.driver.inputText(self.opening_date_from,val)
        
    def input_opening_date_to(self,val):   #开业时间-结束
        self.driver.inputText(self.opening_date_to,val)      
    
    def click_search_button(self):  #点击确认查询按钮
        self.driver.click(self.search_button)
            
    def get_table_data(self):#获取查询结果表格内容
        return self.driver.get_table_content(self.rt_table)
    
    #注销
    def select_logout_button(self,val):#选择点击注销按钮
        #print(self.logout_button%val)
        self.driver.click(self.logout_button%val)        
        
    def select_logout_type(self,val=None):   #注销类型
        itemN = self.driver.getElements(self.logou_type)
        #print(itemN[0])
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)               
            items=items[0].split('\n')
            #print(items)
            val=rdData.getListItem(items)
            #print(val)
        self.driver.selectByText(self.logou_type,val) 

    def input_contents(self,val=''):   #填写注销原因
        self.driver.inputText(self.contents,val)
 
    def click_confirm_button(self): #点击注销确认按钮
        self.driver.click(self.confirm_button)        
        
    def logout_success_name_is_enabled(self):#注销提交后，成功信息是否可见
        return self.driver.findElement(self.logout_success_name)
    
    def get_fail_text(self):#失败信息
        return self.driver.getText(self.logout_fail_name)
        
        
        
        
        