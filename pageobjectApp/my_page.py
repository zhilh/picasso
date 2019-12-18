#-*- coding:utf-8 -*-
'''
Created on 2019年7月15日
@author: zhilh
Description: 我 页面元素封装
'''


class pageElements():
    u'''我 页面'''
    def __init__(self,driver):
        self.driver = driver
        #我
        self.my_='resource_id=>lv_my'    #我 功能按钮
        self.my_title="class=>android.widget.TextView"    #我 页面标题
        self.set_='resource_id=>tv_set' #设置功能按钮
        
        #我-设置
        self.set_title='resource_id=>mainheader_title'   #设置页面标题
        self.set_back='resource_id=>mainheader_leftimg' #设置页面，返回上一步功能按钮
        self.set_pmma='resource_id=>relative_pmma' #设定锁屏密码功能链接
        self.set_qchc='resource_id=>relative_qchc' #清除缓存功能链接
        self.set_xgmm='resource_id=>relative_xgmm' #修改密码功能链接
        self.set_gywm='resource_id=>relative_gywm' #关于功能链接
        self.logout='resource_id=>btn_logout'    #退出登录功能按钮
        
        #我-设置-退出登录        
        self.sure='resource_id=>dialog_bt_sure' #弹框确认按钮
        
        #我-设置-修改密码
        self.xgmm_title='resource_id=>mainheader_title' #修改密码页面标题
        self.xgmm_back='resource_id=>mainheader_leftimg' #修改密码页面，返回上一步功能按钮
        self.xgmm_pa1='resource_id=>xgmm_pa1' #原始密码       
        self.xgmm_pa2='resource_id=>xgmm_pa2' #新密码       
        self.xgmm_pa3='resource_id=>xgmm_pa3' #确认新密码       
        self.xgmm_bt='resource_id=>xgmm_bt' #确认修改按钮       
            
    def click_my_button(self):    #点击我 功能按钮
        self.driver.click(self.my_)
                      
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
    

        
    