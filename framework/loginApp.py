#-*- coding:utf-8 -*-
'''
Created on 2019年6月11日
@author: zhilh
Description: 通用app登录功能
'''

class loginGo():
    '''登录类封装'''
    def __init__(self,driver):
        '''登录页面元素'''
        self.login_name='resource_id=>et_phone'
        self.password='resource_id=>et_password'
        self.login_button='resource_id=>btn_login'
        '''主页-退出 页面元素'''
        self.my='resource_id=>lv_my'
        self.set='resource_id=>tv_set'
        self.logout='resource_id=>btn_logout'
        self.sure='resource_id=>dialog_bt_sure'
        self.driver = driver
        self.cf_login_user=driver.login_user
        self.cf_login_pass=driver.login_pass
        
    def login_(self,username=None,userPwd=None):
        if username==None:
            username = self.cf_login_user
        if userPwd==None:
            userPwd = self.cf_login_pass
            
        self.driver.inputText(self.login_name,username)
        self.driver.inputText(self.password,userPwd)
        self.driver.click(self.login_button)
        #self.driver.waitSleep(3)
        #self.driver.getScreenshot('Apptest')        
        
    def logout_(self):
        self.driver.click(self.my)
        self.driver.click(self.set)
        self.driver.click(self.logout)
        self.driver.click(self.sure)
        self.driver.quit()


