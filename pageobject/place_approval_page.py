#-*- coding:utf-8 -*-
'''
Created on 2018年12月14日
@author: zhilh
Description: 企业备案审核页面元素封装
'''



MAIN_IFRAME='id=>main-iframe'  #主窗口

class placeHome(object):
    '''
    待审核 场所/企业 列表
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        self.driver=driver
        self.title_name='class=>panel-heading'  #页面左上角标题
        self.rt_table='table-striped'#存放查询结果的表格
        self.approve_btn='xpath=>/html/body/div[2]/div/div[2]/table/tbody/tr[%d]/td[8]/button[2]'#审核按钮，每条数据的审核按钮定位根据tr值

    def get_page_title(self):#获取页面标题
        return self.driver.getText(self.title_name)
    
    def get_table_data(self):#获取查询结果表格内容
        return self.driver.get_table_content(self.rt_table)
    
    def select_approve_button(self,val):
        #print(self.approve_btn%val)
        self.driver.click(self.approve_btn%val)        


class placeApprove(object):
    '''
    审核页面
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        self.driver=driver
        self.title_name='xpath=>//*[@id="audit-modal"]/div/div/div[1]/p'  #页面左上角标题
        self.approve_pass='xpath=>//*[@id="audit-modal"]/div/div/div[2]/div/div/form[1]/div/div[2]/div/div/div[1]/label'  #审核结果，通过
        self.approve_no_pass='xpath=>//*[@id="audit-modal"]/div/div/div[2]/div/div/form[1]/div/div[2]/div/div/div[2]/label'  #审核结果，不通过
        self.approve_result='name=>modal-type-box' #审核结果
        self.approve_continue='xpath=>//*[@id="audit-modal"]/div/div/div[2]/div/div/form[1]/div/div[3]/div/div/div[1]/label' #处理方式，继续审核
        self.approve_finish='xpath=>//*[@id="audit-modal"]/div/div/div[2]/div/div/form[1]/div/div[3]/div/div/div[2]/label' #处理方式，审核完成
        self.processing_mode='name=>modal-audit-type' #处理方式
        self.approve_comments='id=>modal-audit-message' #审核意见
        self.approve_button='id=>modal-audit-btn' #审核确认按钮
        self.approve_success_name='xpath=>//*[@id="modal-success"]/div/div/div/p[1]'#审核成功后提示框
        self.approve_fail_name='xpath=>//*[@id="modal-fail"]/div/div/div/p[1]'#审核失败后提示框

 

    def get_page_title(self):#获取页面标题
        return self.driver.getText(self.title_name)
    
    def select_approve_result(self,val):    #选择审核结果
        itemN=self.driver.getElements(self.approve_result)
        for i in itemN:
            #print('text:',i.text)
            if i.text==val:
                i.click()
                
    def select_processing_mode(self,val):    #选择处理方式
        itemN=self.driver.getElements(self.processing_mode)
        for i in itemN:
            #print('text:',i.text)
            if i.text==val:
                i.click()
                
    def select_approve_pass(self):  #选择审核通过
        self.driver.click(self.approve_pass)
    
    def select_approve_finish(self):    #选择审核完成
        self.driver.click(self.approve_finish)        
    
    def input_approve_comments(self,val):   #输入审核意见
        self.driver.inputText(self.approve_comments,val)
        
    def click_approve_button(self): #点击审核确认按钮
        self.driver.click(self.approve_button)        
        
    def approve_fail_name_is_enabled(self):#审核提交后，失败信息是否可见
        return self.driver.findElement(self.approve_fail_name)
    
    def approve_success_name_is_enabled(self):#审核提交后，成功信息是否可见
        return self.driver.findElement(self.approve_success_name)
    
    def get_fail_text(self):
        return self.driver.getText(self.approve_fail_name)
        
   
    
    

