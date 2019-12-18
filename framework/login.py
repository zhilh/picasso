#-*- coding:utf-8 -*-
'''

Created on 2018年9月13日

@author: zhilh

'''

from framework.readConfig import ReadConfig
cf=ReadConfig()

class loginGo():
    u'''登录类封装'''
    def __init__(self,driver):
        u'''初始化driver参数'''
        self.login_name='class=>js-login-name'
        self.password='class=>js-login-password'
        self.verify_code_img='class=>verification-img-area'
        self.verify_code='id=>js-verification-code'
        self.login_button='class=>js-login-btn'
        self.login_type='xpath=>/html/body/div/div/div/form/div[4]/div/label[1]'
        
        self.url=cf.get_config('LOCAL_ACCOUNT', 'login_url')
        self.username=cf.get_config('LOCAL_ACCOUNT', 'login_user')
        self.userPwd=cf.get_config('LOCAL_ACCOUNT', 'login_pass')
        
        self.driver = driver
        self.driver.openUrl(self.url)

    def input_data(self):        
        self.driver.inputText(self.login_name,self.username)
        self.driver.inputText(self.password, self.userPwd)
        code=self.driver.readCode(self.verify_code_img)
        self.driver.inputText(self.verify_code, code)
        self.driver.click(self.login_type)
        
    def click_login(self):
        whileNum=1
        w_flag=True
        while w_flag:
            if whileNum >= 5:
                raise NameError('登录失败，程序多次尝试任无法登录系统，请检查账号、密码是否正确')
                break
            self.input_data()
            self.driver.click(self.login_button)
            whileNum = whileNum +1
            w_flag=self.driver.checkAlert()
            
        
        
        
        
        
        
        
        
        