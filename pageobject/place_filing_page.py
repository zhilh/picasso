#-*- coding:utf-8 -*-
'''
Created on 2018年11月13日
@author: zhilh
Description: 企业备案流程页面元素封装
'''
from framework import rdData

MAIN_IFRAME='id=>main-iframe'  #主窗口

class placeIndex(object):
    '''
    企业备案引导页--选择企业类型
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        self.driver=driver
        self.title_name='xpath=>/html/body/div[2]/div/div[1]/h4'  #页面左上角标题
        self.industry_list="xpath=>//div[@class='list-industry-item']"  #行业列表
        self.industry_item="xpath=>/html/body/div[2]/div/div[2]/div[2]/div/ul/li[%d]/div"  #行业列表

    def get_page_title(self):#获取页面标题
        return self.driver.getText(self.title_name)
    
    def select_industry_item(self,val):
        self.driver.click(self.industry_item%val)        
    
    def select_industry(self,val=None):#选择行业
        self.driver.waitSleep(1)
        self.driver.rightClick(self.industry_list)
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
                i.click()   
        return val             

class placeBasicInfo(object):
    '''
    企业备案首页--填写基本信息
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        self.driver=driver       
        #单位基本信息
        self.place_name='class=>js-set-place-name'#单位名称
        self.business_address='class=>js-set-business-address'#单位经营地址
        self.business_geocoder_button='class=>js-get-geocoder-button'#单位地址地图坐标功能按钮
        self.business_geographic_info_button='class=>location-get-geographic-info'#弹出地图框 地图坐标确定修改功能按钮
        self.has_certificate='class=>js-set-has-certificate'#有无证照
        self.opening_date='class=>js-set-opening-date'#开业日期
        self.fax='class=>js-set-fax'#单位传真
        self.web_address='class=>js-set-web-address'#单位网址
        self.phone_number='class=>js-set-phone-number'#单位电话
        self.operating_state='class=>js-set-operating-state'#经营状态
        
        #营业执照信息
        self.uniform_social_credit_code='class=>js-set-uniform-social-credit-code'#统一社会信用代码/注册号
        self.organization_code='class=>js-set-organization-code'#组织机构代码
        self.company_name='class=>js-set-company-name'#营业执照下的单位名称
        self.company_english_name='class=>js-set-company-english-name'#单位英文名称
        self.company_type='class=>js-set-company-type'#单位性质
        self.registered_address='class=>js-set-registered-address'#单位注册地址
        self.issue_date='class=>js-set-issue-date'#发照日期
        self.registered_capital='class=>js-set-registered-capital'#注册资本
        self.establishment_date='class=>js-set-establishment-date'#成立日期
        self.business_from='class=>js-set-business-from'#经营期限-开始
        self.business_to='class=>js-set-business-to'#经营期限-结束
        self.business_checkbox='id=>js-set-business-checkbox'#经营期限-长期
        self.business_scope='class=>js-set-business-scope'#经营范围
        
        #添加主要人员信息
        self.add_practitioner='class=>js-add-practitioner'#添加企业人员按钮
        self.person_position='class=>js-set-position'#职位/工种
        self.person_country='class=>js-set-country'#国家/地区
        self.person_card='class=>js-set-personal-card'#证件类型
        self.person_id_number='class=>js-set-identification-number'#证件号码
        self.person_name='class=>js-set-person-name'#姓名
        self.person_birth_date='class=>js-set-birth-date'#出生日期
        self.person_ethnicity='class=>js-set-ethnicity'#民族
        self.person_address='class=>js-set-permanent-address'#户籍地址
        self.person_issuing_authority='class=>js-set-issuing-authority'#签发机关
        self.person_validity_date_from='class=>js-set-certificate-validity-from-date'#有效期-开始
        self.person_validity_date_to='class=>js-set-certificate-validity-thru-date'#有效期-结束
        self.person_phone_number='class=>js-set-person-phone-number'#手机号码
        self.person_current_address='class=>js-set-current-address'#现住详址
        self.person_save_button='class=>js-save-practitioner'#保存人员功能按钮
        
        
        #管辖信息
        self.region='class=>region-value-area'  #管辖机构
        self.region_input='class=>region-search-tree-box'  #输入机构名称进行过滤
        self.region_search='class=>tree-search-btn'   #管辖机构查询按钮
        self.region_select='xpath=>//*[@id="ztreeid0_1_a"]'    #查询结果的第一个机构名称
        self.region_police='class=>js-set-police'#责任民警
        self.region_police_select='class=>autocomplete-suggestion'    #下拉选项候选民警
        self.region_phone='class=>js-set-office-phone-number'#机构办公电话
        
        self.second_step='class=>js-second-step'#下一步按钮
        
    
    ####场所基本信息#####
    def input_place_name(self,val): #输入单位名称
        self.driver.inputText(self.place_name,val)
        return val
        
    def input_business_address(self,val):   #定位单位经营地址
        self.driver.inputText(self.business_address,val)
        self.driver.click(self.business_geocoder_button)
        self.driver.waitSleep(1)
        self.driver.click(self.business_geographic_info_button)
        
    def select_has_certificate(self,val=None):  #有无证照
        itemN = self.driver.getElements(self.has_certificate)
        #print(self.has_certificate,itemN[0])
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)               
            items=items[0].split('\n')
            #print(items)
            val=rdData.getListItem(items)
            #print(val)        
        self.driver.selectByText(self.has_certificate,val)
        
    def input_opening_date(self,val):  #开业日期
        self.driver.inputText(self.opening_date,val)
        self.driver.click(self.place_name)#点击页面任意一个输入框，消除弹出的日期控件
        
    def input_fax(self,val):  #单位传真
        self.driver.inputText(self.fax,val)
        
    def input_web_address(self,val):  #单位网址
        self.driver.inputText(self.web_address,val)
        
    def input_phone_number(self,val):  #单位电话        
        self.driver.inputText(self.phone_number,val)
        
    def select_operating_state(self,val=None):  #经营状态
        itemN = self.driver.getElements(self.operating_state)
        #print(self.operating_state,itemN[0])
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)               
            items=items[0].split('\n')
            #print(items)
            val=rdData.getListItem(items)
            #print(val)        
        self.driver.selectByText(self.operating_state,val)

    ####营业执照信息####
    def input_uniform_social_credit_code(self,val):  #统一社会信用代码/注册号
        self.driver.inputText(self.uniform_social_credit_code,val)

    def input_organization_code(self,val):  #组织机构代码
        self.driver.inputText(self.organization_code,val)

    def input_company_name(self,val):  #单位名称
        self.driver.inputText(self.company_name,val)

    def input_company_english_name(self,val):  #单位英文名称
        self.driver.inputText(self.company_english_name,val)

    def select_company_type(self,val=None):  #单位性质
        itemN = self.driver.getElements(self.company_type)
        #print(itemN[0])
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)               
            items=items[0].split('\n')
            #print(items)
            val=rdData.getListItem(items)
            #print(val)
        self.driver.selectByText(self.company_type,val)        

    def input_registered_address(self,val):  #单位注册地址
        self.driver.inputText(self.registered_address,val)
        
    def input_issue_date(self,val):  #发照日期
        self.driver.inputText(self.issue_date,val)
        self.driver.click(self.place_name)#点击页面任意一个输入框，消除弹出的日期控件
        
    def input_registered_capital(self,val):  #注册资本
        self.driver.inputText(self.registered_capital,val)
        
    def input_establishment_date(self,val):  #成立日期
        self.driver.inputText(self.establishment_date,val)
        self.driver.click(self.place_name)#点击页面任意一个输入框，消除弹出的日期控件
        
    def input_business_from(self,val):  #经营期限-开始
        self.driver.inputText(self.business_from,val)
        self.driver.click(self.place_name)#点击页面任意一个输入框，消除弹出的日期控件
        
    def input_business_to(self,val):  #经营期限-结束
        self.driver.inputText(self.business_to,val)
        self.driver.click(self.place_name)#点击页面任意一个输入框，消除弹出的日期控件

    def input_business_checkbox(self,val):  #经营期限-长期
        self.driver.click(self.business_checkbox,val)
        
    def input_business_scope(self,val):  #经营范围
        self.driver.inputText(self.business_scope,val)

    ####人员信息#####
    def click_add_practitioner(self):#点击添加人员按钮
        self.driver.click(self.add_practitioner)

    def select_person_position(self,val=None): #职位/工种
        itemN = self.driver.getElements(self.person_position)
        #print(itemN[0])
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)               
            items=items[0].split('\n')
            #print(items)
            val=rdData.getListItem(items)
            #print(val)
        self.driver.selectByText(self.person_position,val)

    def select_person_country(self,val=None): #国家/地区
        itemN = self.driver.getElements(self.person_country)
        #print(itemN[0])
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)               
            items=items[0].split('\n')
            #print(items)
            val=rdData.getListItem(items)
            #print(val)
        self.driver.selectByText(self.person_country,val)

    def select_person_card(self,val=None):  #证件类型
        itemN = self.driver.getElements(self.person_card)
        #print(itemN[0])
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)               
            items=items[0].split('\n')
            #print(items)
            val=rdData.getListItem(items)
            #print(val)
        self.driver.selectByText(self.person_card,val)

    def input_person_id_number(self,val):  #证件号码
        self.driver.inputText(self.person_id_number,val)

    def input_person_name(self,val):  #姓名
        self.driver.inputText(self.person_name,val)

    def input_person_birth_date(self,val):  #出生日期
        self.driver.inputText(self.person_birth_date,val)
        self.driver.click(self.person_name)#点击页面任意一个输入框，消除弹出的日期控件

    def select_person_ethnicity(self,val=None):  #民族
        itemN = self.driver.getElements(self.person_ethnicity)
        #print(itemN[0])
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)               
            items=items[0].split('\n')
            #print(items)
            val=rdData.getListItem(items)
            #print(val)
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

    def input_person_current_address(self,val):  #现住详址
        self.driver.inputText(self.person_current_address,val)

    def click_person_save_button(self):  #点击保存人员按钮
        self.driver.click(self.person_save_button)

    
    ####管辖信息#####
    def select_region(self,val):#管辖机构,选择当前登录用户所在机构
        self.driver.waitSleep(1)
        self.driver.click(self.region)
        self.driver.inputText(self.region_input,val)
        self.driver.click(self.region_search)
        self.driver.click(self.region_input)#这里点击操作是避免出现'stale element reference: element is not attached to the page document'的问题
        self.driver.click(self.region_select)
     
    def input_region_police(self,val):#责任民警，选择当前登录用户
        self.driver.waitSleep(1)
        self.driver.click(self.region_police)
        itemN = self.driver.getElements(self.region_police_select)
        for i in itemN:
            if i.text.count(val)>0:
                i.click() 

    
    def input_region_phone(self,val):#机构办公电话，如果这个栏位没有默认值，则填入随机电话号码
        self.driver.inputText(self.region_phone,val)
    
    def click_second_step(self):  #点击下一步按钮
        self.driver.click(self.second_step)


class placeExtras(object):
    '''
    企业备案第二页--填写附加信息
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        self.driver=driver       
        self.page_title='xpath=>/html/body/div[2]/div/div[1]/h4'  #页面标题
        self.third_step='class=>js-third-step'  #下一步功能按钮
        
        #危化业-企业信息 =========================
        #self.chemistry_place_type='name=>chemistry-place-type'#企业类型
        self.chemistry_place_type='xpath=>//div[@class="form-horizontal-input-area place-weihua-type-area"]/div/label'#单位类型        
        #self.chemistry_involve_type='name=>chemistry-involve-type'  #涉及环节
        self.chemistry_involve_type='xpath=>//div[@class="form-horizontal-input-area involve-type-area"]/div/label'  #涉及环节
        self.danger_level='class=>js-set-danger-level'  #存放危险等级
        self.weihua_office_phone_number='class=>js-set-weihua-office-phone-number'  #值班室电话
        self.weihua_monitor_phone_number='class=>js-set-weihua-monitor-phone-number'  #监控室电话        
        #危化业-企业涉及物品
        self.product_name='class=>js-product-name' #危化品输入框
        self.product_name_list='class=>autocomplete-suggestion' #危化品名称列表
        self.product_add_btn='class=>btn btn-default js-add-product'#危化品添加按钮
        #危化业-危化品仓库
        self.warehouse_name='class=>js-set-warehouse-name'#仓库名称
        self.warehouse_address='class=>js-address-chemistry'#仓库地址
        self.warehouse_coordinate='class=>js-location-chemistry'#仓库地址坐标按钮
        self.warehouse_geographic_info_button='class=>location-get-geographic-info'#弹出地图框 地图坐标确定修改功能按钮
        self.warehouse_img='class=>file-item-box'#上传仓库平面图
        self.warehouse_upload='xpath=>//input[@class="file-item-box"]'#上传仓库平面图 上传按钮
        self.warehouse_IMEI='class=>js-set-door-lock-number'#仓库门锁IMEI码btn btn-default pull-right add-button js-add-attachment
        self.warehouse_add_btn='class=>add-warehouse-btn'#添加仓库按钮
        #===================================
                
        #旅馆业-企业信息 ======================
        #房间信息
        self.hotel_building_area='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[3]/div[1]/div/div/input'#建筑总面积
        self.hotel_business_area='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[3]/div[2]/div/div/input'#营业面积
        self.hotel_balcony_area='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[3]/div[3]/div/div/input'#包厢面积
        self.hotel_building_count='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[3]/div[4]/div/div/input'#楼栋数
        self.hotel_floor_count='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[3]/div[5]/div/div/input'#楼层数
        self.hotel_room_count='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[3]/div[6]/div/div/input'#房间总数
        self.hotel_bed_count='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[3]/div[7]/div/div/input'#核定内容
        #视频监控探头信息
        self.hotel_gateway_count='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[4]/div[1]/div/div/input'#出入口
        self.hotel_selling_area='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[4]/div[2]/div/div/input'#营业厅
        self.hotel_passageway_count='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[4]/div[3]/div/div/input'#通道
        self.hotel_storehouse_count='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[4]/div[4]/div/div/input'#保管库房
        self.hotel_parking_lot='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[4]/div[5]/div/div/input'#停车场        
        self.hotel_other_part='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[4]/div[6]/div/div/input'#其他部位
        #==================================
        
        #保安服务业-企业信息==================
        self.special_number='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[1]/div[1]/div/input' #特行许可证号
        self.special_issuing_authority='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[1]/div[2]/div/input' #发证机关
        self.special_issuing_date='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[1]/div[3]/div/input' #发证日期
        self.special_licence_always_valid='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[1]/div[4]/div/div[2]/label/input' #证件有效期 长期有效
        #==================================
        
        #娱乐业-企业信息======================
        self.fire_safety_responsibility_number='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[2]/div[1]/div/input'#消防安全责任书号
        self.hygienic_license_number='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[2]/div[2]/div/input'#卫生许可证号
        self.housing_safety_approval_number='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[2]/div[3]/div/input'#房屋安全审定书号
        self.environmental_department_document='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[2]/div[4]/div/input'#环保部门批准文件
        self.yule_business_area='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[2]/div[5]/div/input'#营业面积
        self.yule_balcony_count='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[2]/div[6]/div/input'#包厢数
        self.safety_equipment='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[2]/div[7]/div/input'#技防设备
        self.fire_fighting_device='xpath=>/html/body/div[2]/div/div[2]/div[3]/form[1]/div[2]/fieldset[2]/div[8]/div/input'#消防设施        
        #=================================
  
    def get_secondPage_title(self):#获取页面标题
        return self.driver.getText(self.page_title)
    def click_third_step(self): #点击下一步按钮
        self.driver.click(self.third_step)
    
    #娱乐业操作
    def input_fire_safety_responsibility_number(self,val=rdData.getStrings(20)):#消防安全责任书号
        self.driver.inputText(self.fire_safety_responsibility_number,val) 
    def input_hygienic_license_number(self,val=rdData.getStrings(20)):#卫生许可证号
        self.driver.inputText(self.hygienic_license_number,val) 
    def input_housing_safety_approval_number(self,val=rdData.getStrings(20)):#房屋安全审定书号
        self.driver.inputText(self.housing_safety_approval_number,val) 
    def input_environmental_department_document(self,val=rdData.getStrings(20)):#环保部门批准文件
        self.driver.inputText(self.environmental_department_document,val) 
    def input_yule_business_area(self,val=rdData.getInt(3)):#营业面积
        self.driver.inputText(self.yule_business_area,val) 
    def input_yule_balcony_count(self,val=rdData.getInt(2)):#包厢数
        self.driver.inputText(self.yule_balcony_count,val) 
    def input_safety_equipment(self,val=rdData.getGBK2312(20)):#技防设备
        self.driver.inputText(self.safety_equipment,val) 
    def input_fire_fighting_device(self,val=rdData.getGBK2312(20)):#消防设施
        self.driver.inputText(self.fire_fighting_device,val) 
    
    #保安服务业操作
    def input_special_number(self,val=rdData.getStrings(20)): #特行许可证号
        self.driver.inputText(self.special_number,val) 
    def input_special_issuing_authority(self,val=rdData.getGBK2312(8)): #发证机关
        self.driver.inputText(self.special_issuing_authority,val) 
    def input_special_issuing_date(self,val=rdData.getDate(-100, 0)): #发证日期
        self.driver.inputText(self.special_issuing_date,val) 
    def click_special_licence_always_valid(self): #证件有效期 长期有效
        self.driver.click(self.special_licence_always_valid)     
        
    #旅馆业操作
    def input_hotel_building_area(self,val=rdData.getInt(5)): #建筑总面积
        self.driver.inputText(self.hotel_building_area,val) 
    def input_hotel_business_area(self,val=rdData.getInt(4)): #营业面积
        self.driver.inputText(self.hotel_business_area,val) 
    def input_hotel_balcony_area(self,val=rdData.getInt(3)): #包厢面积
        self.driver.inputText(self.hotel_balcony_area,val) 
    def input_hotel_building_count(self,val=rdData.getInt(1)): #楼栋数
        self.driver.inputText(self.hotel_building_count,val) 
    def input_hotel_floor_count(self,val=rdData.getInt(2)): #楼层数
        self.driver.inputText(self.hotel_floor_count,val) 
    def input_hotel_room_count(self,val=rdData.getInt(3)): #房间总数
        self.driver.inputText(self.hotel_room_count,val) 
    def input_hotel_bed_count(self,val=rdData.getInt(4)): #核定内容
        self.driver.inputText(self.hotel_bed_count,val) 
    def input_hotel_gateway_count(self,val=rdData.getInt(1)): #出入口
        self.driver.inputText(self.hotel_gateway_count,val) 
    def input_hotel_selling_area(self,val=rdData.getInt(1)): #营业厅
        self.driver.inputText(self.hotel_selling_area,val) 
    def input_hotel_passageway_count(self,val=rdData.getInt(1)):  #通道
        self.driver.inputText(self.hotel_passageway_count,val) 
    def input_hotel_storehouse_count(self,val=rdData.getInt(1)): #保管库房
        self.driver.inputText(self.hotel_storehouse_count,val) 
    def input_hotel_parking_lot(self,val=rdData.getInt(1)): #停车场
        self.driver.inputText(self.hotel_parking_lot,val) 
    def input_hotel_other_part(self,val=rdData.getInt(1)): #其他部位
        self.driver.inputText(self.hotel_other_part,val) 
        
    #危化业操作      
    def select_chemistry_place_type(self,val=None):    #企业类型
        itemN = self.driver.getElements((self.chemistry_place_type))
        #print(itemN)
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)   
            #print(items)
            val=rdData.getListItem(items,len(items)+1)
        for i in itemN:
            if val.count(i.text)>0:
                i.click()         
    def select_chemistry_involve_type(self,val=None):    #涉及环节
        itemN = self.driver.getElements((self.chemistry_involve_type))
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)   
            #print(items)
            val=rdData.getListItem(items,len(items)+1)
        for i in itemN:
            if val.count(i.text)>0:
                i.click()         
    def select_danger_level(self,val=None):  #存放危险等级
        itemN = self.driver.getElements(self.danger_level)
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)               
            items=items[0].split('\n')
            #print(items)
            val=rdData.getListItem(items)
            #print(val)
        self.driver.selectByText(self.danger_level,val)
    def input_weihua_office_phone_number(self,val): #值班室电话
        self.driver.inputText(self.weihua_office_phone_number,val)        
    def input_weihua_monitor_phone_number(self,val):    #监控室电话
        self.driver.inputText(self.weihua_monitor_phone_number,val)
    def input_product_name(self,val=None):#危化产品
        self.driver.click(self.product_name)
        self.driver.waitSleep(1)
        itemN = self.driver.getElements(self.product_name_list)
        self.driver.waitSleep(1)
        print(itemN)
        if val==None:
            items=[]
            for i in itemN:
                items.append(i.text)               
            #items=items[0].split('\n')
            print(items)
            val=rdData.getListItem(items)
            print(val)
        for i in itemN:
            if i.text.count(val)>0:
                i.click() 
    def click_product_add_btn(self): #点击添加危化品按钮
        self.driver.click(self.product_add_btn)
    def input_warehouse_name(self,val):    #仓库名称
        self.driver.inputText(self.warehouse_name,val)        
    def input_warehouse_address(self,val):    #仓库地址
        self.driver.inputText(self.warehouse_address,val)
        self.driver.click(self.warehouse_coordinate)
        self.driver.waitSleep(1)
        self.driver.click(self.warehouse_geographic_info_button)        
    def upload_warehouse_img(self,att):#上传仓库平面图
        self.driver.waitSleep(1)
        itemN = self.driver.getElements(self.warehouse_upload)
        print(itemN)
        for i in itemN:
            print(i)
            self.driver.waitSleep(1)
            i.click() 
            break
        self.driver.upload_att(self.warehouse_upload,att)                 
    def input_warehouse_IMEI(self,val):    #仓库IMEI
        self.driver.inputText(self.warehouse_IMEI,val)        
    def click_warehouse_add_btn(self): #点击添加仓库
        self.driver.click(self.warehouse_add_btn)
     
class placeDevices(object):
    '''
    企业备案第三页--填写设备信息
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        self.driver=driver
        self.device_name='class=>js-set-device-name'  #设备名称
        self.device_count='class=>js-set-device-count'  #设备数量
        self.save_button='class=>js-save-button'  #保存功能按钮
        self.place_success_name='class=>modal-success'  #备案成功后提示框

    def input_device_name(self,val):    #设备名称
        self.driver.inputText(self.device_name,val)
        
    def input_device_count(self,val):   #设备数量
        self.driver.inputText(self.device_count,val)

    def click_save_button(self):  #点击保存功能按钮
        self.driver.click(self.save_button)
            
    def place_success_name_is_enabled(self):#判断备案提交后，成功信息是否可见
        return self.driver.findElement(self.place_success_name)
                
        
        
