#-*- coding:utf-8 -*-
'''
Created on 2019年1月31日
@author: zhilh
Description: 人员注销页面封装
'''


MAIN_IFRAME='id=>main-iframe'  #主窗口

class pageElements(object):
    '''
    从业人员注销页面元素
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        self.driver=driver
        self.title_name='class=>panel-heading'  #首页标题
                
        self.place_name='class=>js-set-place-name'  #所属企业名称
        self.person_name='class=>js-set-name'  #人员名称
        self.person_id_card='class=>js-set-identification-number'  #人员证件号码
        
        self.select_industry_btn='class=>bs-placeholder' #选择所属行业按钮
        self.industrys='class=>text'#所属行业列表
        self.apply_date_from='class=>js-set-apply-date-from'#备案申请时间-开始
        self.apply_date_to='class=>js-set-apply-date-thru'#备案申请时间-结束
        
        self.region='class=>region-value-area'  #管辖机构
        self.region_input='class=>region-search-tree-box'  #机构名称输入框
        self.select_all='class=>select-all-tree-btn'  #全选
        self.select_clear='class=>quit-select-all-tree-btn'   #清除
        self.region_search='class=>tree-search-btn'   #管辖机构查询按钮         
        self.set_age_from='class=>js-set-age-from'#年龄范围-开始
        self.set_age_to='class=>js-set-age-thru'    #年龄范围-结束

        self.phone_number='class=>js-set-phone-number'  #联系电话
        self.select_status_btn='class=>bs-placeholder' #选择审核状态按钮
        self.status='class=>text'#审核状态列表
        self.person_sex='xpath=>/html/body/div[4]/div/div[2]/form/fieldset/div[6]/div[8]/div/label'  #人员性别
        #self.person_sex='name=>sex'  #人员性别
        
        self.search_button='class=>js-search-button'  #确认查询        
        self.rows='class=>text-primary'#查询结果显示条数
        self.rt_table='table-striped'#存放查询结果的表格
        self.logout_button='xpath=>//*[@class="js-search-results-tbody"]/tr[%d]/td[9]/button'#注销按钮，每条数据的注销按钮定位根据tr值
        
        #注销弹框
        self.contents='class=>js-logout-reason-content'#注销原因
        self.confirm_button='class=>js-confirm-logout'  #确认注销
        self.logout_success_name='xpath=>//*[@id="modal-success"]/div/div/div/p[1]'#成功后提示框
        self.logout_fail_name='xpath=>//*[@id="modal-fail"]/div/div/div/p[1]'#失败后提示框
        
    
    def get_title_name(self):   #获取页面标题
        self.driver.getText(self.title_name)
        
    def input_place_name(self,val):   #所属企业名称
        self.driver.inputText(self.place_name,val)
    def input_person_name(self,val):   #人员名称
        self.driver.inputText(self.person_name,val)
    def input_person_id_card(self,val):   #人员证件号码
        self.driver.inputText(self.person_id_card,val)

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
    def input_apply_date_from(self,val):   #备案申请时间-开始
        self.driver.inputText(self.apply_date_from,val)
    def input_apply_date_to(self,val):   #备案申请时间-结束
        self.driver.inputText(self.apply_date_to,val)

    def select_region_name(self,val):  #管辖机构
        self.driver.click(self.region)
        self.driver.click(self.select_clear)
        self.driver.inputText(self.region_input,val)
        self.driver.click(self.region_search)
        self.driver.click(self.select_all)        
    def input_set_age_from(self,val):   #年龄范围-开始
        self.driver.inputText(self.set_age_from,val)        
    def input_set_age_to(self,val):   #年龄范围-结束
        self.driver.inputText(self.set_age_to,val)
        
    def input_phone_number(self,val):   #联系电话
        self.driver.inputText(self.phone_number,val)
    def select_status(self,val):   #审核状态
        self.driver.click(self.select_status_btn)
        elet_list = self.driver.getElements(self.status) 
        if val == None or val.strip()=='':
            val='[]'
        vals=eval(val)
        for i in range(len(elet_list)):
            for j in vals:
                #print(elet_list[i].text,j)
                if elet_list[i].text==j:
                    elet_list[i].click()
    def select_person_sex(self,val=None):    #人员性别
        itemN = self.driver.getElements((self.person_sex))
        #print(len(itemN),itemN)
        '''
        if val==None or val.strip()=='':
            items=[]
            for i in itemN:
                items.append(i.text)  
            #items=items[0].split('\n')             
            #print('items: ',items)
            val=rdData.getListItem(items)
            #print('val: ',val)
         '''
        if  val != None :
            for i in itemN:
                if val.count(i.text)>0:
                    i.click()
                    break
    
    def click_search_button(self):  #点击确认查询按钮
        self.driver.click(self.search_button)
            
    def get_table_data(self):#获取查询结果表格内容
        return self.driver.get_table_content(self.rt_table)
        
    def select_logout_button(self,val):#选择点击注销按钮
        #print(self.logout_button%val)
        self.driver.click(self.logout_button%val)        
        
    def input_contents(self,val=''):   #填写注销原因
        self.driver.inputText(self.contents,val)
 
    def click_confirm_button(self): #点击注销确认按钮
        self.driver.click(self.confirm_button)        
        
    def logout_success_name_is_enabled(self):#注销提交后，成功信息是否可见
        return self.driver.findElement(self.logout_success_name)
    
    def get_fail_text(self):#失败信息
        return self.driver.getText(self.logout_fail_name)
        
        