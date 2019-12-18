#-*- coding:utf-8 -*-
'''
Created on 2018年12月7日
@author: zhilh
Description: 主页左边菜单元素封装
'''

class leftPage(object):
    '''
    主页菜单页面元素
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        #顶部菜单
        self.driver=driver
        self.login_name='class=>navbar-region'  #登录账户名称
        self.node_name='class=>navbar-name'  #登录账户所属机构名称
        self.login_out='class=>js-quit-login-btn'   #退出登录
        self.home_icon='xpath=>/html/body/div[1]/header/div/a/span[3]' #首页链接
        #self.modify_password='class=>navbar-href-btn'   #修改登录账号密码
        self.modify_password='xpath=>/html/body/div[1]/header/div/div/ul[2]/li/ul/li[1]/a'   #修改登录账号密码
        self.mail_link='class=>icon-navbar-mail' #待办事项链接
        self.news_link='class=>icon-navbar-news' #信息列表链接
        
        #左边菜单
        self.DWGL_link='xpath=>//*[@id="side-menu0"]/li[2]/a'    #企业管理
        self.DWXZ_link='xpath=>//*[@id="side-menu10101"]'    #企业新增
        self.DWSH_link='xpath=>//*[@id="side-menu10102"]'    #企业审核
        self.DWBG_link='xpath=>//*[@id="side-menu10103"]'    #企业变更
        self.DWZX_link='xpath=>//*[@id="side-menu10104"]'    #企业注销
        self.DWCX_link='xpath=>//*[@id="side-menu10105"]'    #企业综合查询
        
        self.RYGL_link='xpath=>//*[@id="side-menu0"]/li[3]/a'    #人员管理
        self.RYXZ_link='xpath=>//*[@id="side-menu10201"]'    #人员新增
        self.RYBG_link='xpath=>//*[@id="side-menu10202"]'    #人员变更
        self.RYZX_link='xpath=>//*[@id="side-menu10203"]'    #人员注销
        self.RYSH_link='xpath=>//*[@id="side-menu10204"]'    #人员审核
        self.RYCX_link='xpath=>//*[@id="side-menu10205"]'    #人员查询
       
        self.DWJC_link='xpath=>//*[@id="side-menu103"]'    #单位检查
        
        self.JCTJ_link='xpath=>//*[@id="side-menu104"]'    #检查统计
        
        self.QBYP_link='xpath=>/html/body/div[2]/div[1]/div/ul/li[6]/a'    #情报研判        
        self.QJQBJS_link='xpath=>//*[@id="side-menu10501"]'    #全警情报检索
        self.BJCX_link='xpath=>//*[@id="side-menu10502"]'    #报警查询
        self.CSSPJK_link='xpath=>//*[@id="side-menu10503"]'    #场所视频监控
        self.CSSPHF_link='xpath=>//*[@id="side-menu10504"]'    #场所视频回放
        
        self.XXFB_menu_link='xpath=>/html/body/div[2]/div[1]/div/ul/li[7]/a'    #信息发布
        self.XXFB_link='xpath=>//*[@id="side-menu10601"]'    #信息发布
        self.FBLSCX_link='xpath=>//*[@id="side-menu10602"]'    #发布历史查询
        
        self.XTSZ_link='xpath=>/html/body/div[2]/div[1]/div/ul/li[8]/a'    #系统设置
        self.JGGL_link='xpath=>//*[@id="side-menu10701"]'    #机构管理
        self.YHGL_link='xpath=>//*[@id="side-menu10702"]'    #用户管理
        self.YHZGL_link='xpath=>//*[@id="side-menu10703"]'    #用户组管理
        self.YHFZGL_link='xpath=>//*[@id="side-menu10704"]'    #用户分组管理
        self.DFBSZ_link='xpath=>//*[@id="side-menu10705"]'    #打分表设置
        self.SJZD_link='xpath=>//*[@id="side-menu10706"]'    #数据字典
        self.CSSZ_link='xpath=>//*[@id="side-menu10707"]'    #参数设置
        self.KZSJZD_link='xpath=>//*[@id="side-menu10708"]'    #扩展数据字段
        
        self.Log_link='xpath=>/html/body/div[2]/div[1]/div/ul/li[9]/a'    #日志查看
        self.workLog_link='xpath=>//*[@id="side-menu10801"]'    #工作日志
        self.operationLog_link='xpath=>//*[@id="side-menu10802"]'    #操作日志

        
        
    def get_login_name(self):#登录用户名
        return self.driver.getText(self.login_name)
    
    def get_node_name(self):#登录用户所属机构名
        return self.driver.getText(self.node_name)
    
    def get_page_title(self):#获取页面title
        self.driver.waitSleep()
        return self.driver.getTitle()
        
    def go_modify_password(self):#修改密码
        self.driver.click(self.login_name)
        self.driver.click(self.modify_password)
    
    def go_login_out(self):#退出系统
        self.driver.click(self.login_name)
        self.driver.click(self.login_out)
    
    def go_home(self):
        self.driver.click(self.home_icon)
        
    def go_add_place(self):  #企业新增
        self.go_home()
        self.driver.click(self.DWGL_link)
        self.driver.click(self.DWXZ_link)

    def go_add_person(self):  #人员新增
        self.go_home()
        self.driver.click(self.RYGL_link)
        self.driver.click(self.RYXZ_link)

    def go_approve_person(self):  #人员审核
        self.go_home()
        self.driver.click(self.RYGL_link)
        self.driver.click(self.RYSH_link)

    def go_approve_place(self):  #备案企业审核
        self.go_home()
        self.driver.click(self.DWGL_link)
        self.driver.click(self.DWSH_link)
        
    def go_place_query(self):  #企业综合查询
        self.go_home()
        self.driver.click(self.DWGL_link)
        self.driver.click(self.DWCX_link)

    def go_person_query(self):  #从业人员查询
        self.go_home()
        self.driver.click(self.RYGL_link)
        self.driver.click(self.RYCX_link)

    def go_person_logout(self):  #人员注销
        self.go_home()
        self.driver.click(self.RYGL_link)
        self.driver.click(self.RYZX_link)
        
    def go_place_logout(self):  #企业注销
        self.go_home()
        self.driver.click(self.DWGL_link)
        self.driver.click(self.DWZX_link)

    def go_person_modify(self):  #人员变更
        self.go_home()
        self.driver.click(self.RYGL_link)
        self.driver.click(self.RYBG_link)

    def go_place_modify(self):  #企业变更
        self.go_home()
        self.driver.click(self.DWGL_link)
        self.driver.click(self.DWBG_link)



