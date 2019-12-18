#-*- coding:utf-8 -*-
'''
Created on 2019年7月11日
@author: zhilh
Description: 联系人页面元素封装
'''


class pageElements():
    u'''联系人页面'''
    def __init__(self,driver):
        self.driver = driver
        #联系人
        self.contacts='resource_id=>lv_contacts'    #联系人功能按钮
        self.contacts_title="class=>android.widget.TextView"    #联系人页面标题
        
        #联系人-添加好友
        self.add='resource_id=>tv_add' #添加好友功能按钮
        self.mainheader_title='resource_id=>mainheader_title'   #添加好友页面标题 或者 新的朋友页面页面标题
        self.back_main='resource_id=>mainheader_leftimg' #在添加好友页面或者新的朋友页面，返回到联系人页面功能按钮
        
        #联系人-新的朋友
        self.newfriends='resource_id=>rv_newfriends'    #新的朋友功能按钮
        
        #联系人-我的群聊
        self.mychats='resource_id=>lv_mychats' #我的群聊功能按钮
        self.chat_name='resource_id=>chat_name' #我的群聊页面标题
        self.chat_back='resource_id=>btn_chat_back' #在我的群聊页，返回到联系人页面功能按钮        
            
    def click_contacts_button(self):    #点击联系人功能按钮
        self.driver.click(self.contacts)
                      
    def click_add_button(self):   #点击添加好友功能按钮
        self.driver.click(self.add)        
    def click_back_main_button(self):   #在添加好友页面 或者 新的朋友页面，点击返回到联系人页面功能按钮
        self.driver.click(self.back_main)

    def click_newfriends_button(self):   #点击新的朋友功能按钮
        self.driver.click(self.newfriends)        
        
    def click_mychats_button(self):   #点击我的群聊功能按钮
        self.driver.click(self.mychats)    
    def click_chat_back_button(self):   #在我的群聊页，点击返回到联系人页面功能按钮
        self.driver.click(self.chat_back)    
        
    def find_element_contacts_title(self):  #获取联系人页面标题
        return self.driver.getText(self.contacts_title)
    def find_element_add_title(self):   #获取添加好友页面标题
        return self.driver.getText(self.mainheader_title)
    def find_element_newfriends_title(self):    #获取新的朋友页面标题
        return self.driver.getText(self.mainheader_title)
    def find_element_chat_name_title(self):  #获取我的群聊页面标题
        return self.driver.getText(self.chat_name)
    

        
    