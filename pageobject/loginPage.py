#-*- coding:utf-8 -*-
'''

Created on 2018年9月8日

@author: zhilh

'''


class pageElements():
    u'''登录页面'''
    def __init__(self,driver):
        u'''初始化driver参数'''
        self.login_url='http://192.168.0.234/picasso-lan-web-source/public/assets/governance/v1/sessions_new.html'
        self.login_name='class=>js-login-name'
        self.password='class=>js-login-password'
        self.verify_code_img='class=>verification-img-area'
        self.verify_code='id=>js-verification-code'
        self.login_button='class=>js-login-btn'
        self.login_type='xpath=>/html/body/div/div/div/form/div[4]/div/label[1]'
        self.driver = driver
                
    def open_browser(self):
        self.driver.openUrl(self.login_url)
    
    def winLocation(self):
        self.driver.js("window.location.href='"+self.login_url+"';return false")
    
    def input_login_name(self,login_name):
        self.driver.inputText(self.login_name, login_name)
    
    def input_password(self,password):
        self.driver.inputText(self.password, password)
        
    def input_verify_code(self):
        code=self.driver.readCode(self.verify_code_img)
        self.driver.inputText(self.verify_code,code)
    
    def click_login_type(self): 
        self.driver.click(self.login_type)
         
    def click_login_button(self):
        self.driver.click(self.login_button)
        self.driver.checkAlert()
    
    def get_page_title(self):
        return self.driver.getTitle()
    
    
    def quit(self):
        self.driver.quit()
        
        
    