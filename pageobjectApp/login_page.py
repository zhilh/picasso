#-*- coding:utf-8 -*-
'''
Created on 2019年7月8日
@author: zhilh
Description: app登录页面封装
'''


class pageElements():
    u'''登录页面'''
    def __init__(self,driver):
        self.login_name='resource_id=>et_phone'
        self.password='resource_id=>et_password'
        self.login_button='resource_id=>btn_login'
        self.my='resource_id=>lv_my'    #登录后的首页元素，用于验证登录是否成功
        self.driver = driver
                    
    def input_login_name(self,login_name):
        self.driver.inputText(self.login_name, login_name)
    
    def input_password(self,password):
        self.driver.inputText(self.password, password)
                 
    def click_login_button(self):
        self.driver.click(self.login_button)
    
    def find_element(self):
        return self.driver.findElement(self.my)
    

        
    