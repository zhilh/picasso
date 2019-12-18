#-*- coding:utf-8 -*-
'''
Created on 2018年11月13日
@author: zhilh
Description: 
'''
class pageElements(object):
    '''
    企业备案首页--选择企业类型
    '''
    def __init__(self, driver):
        '''
        初始化页面元素
        '''
        self.driver=driver
        self.main_iframe='id=>main-iframe'  #主窗口
        self.title_name='class=>panel-heading'  #首页标题
        self.JiDi='class=>js-industry-jidi'  #寄递业
        self.QiTa='class=>js-industry-qita'  #其他
        self.GongZhang='class=>js-industry-gongzhang'  #公章刻制业
        self.YuLe='class=>js-industry-yule'  #公共娱乐服务场所
        self.LvGuan='class=>js-industry-lvguan'  #旅馆业
        self.KaiSuo='class=>js-industry-kaisuo'  #开锁业
        self.BaoAn='class=>js-industry-baoan'  #保安服务业
        self.YinShua='class=>js-industry-yinshua'  #印刷业
        self.SheBao='class=>js-industry-weihua'  #涉爆企业
        self.DianDang='class=>js-industry-diandang'  #典当业
        self.ZhongDian='class=>js-industry-zhongdian'  #重点单位
        self.QiCheZuLin='class=>js-industry-qichezulin'  #汽车租赁业


    def click_JiDi(self):  #点击 寄递业 进入 寄递业 行业备案首页
        self.driver.click(self.JiDi)
        
    def click_QiTa(self):  #点击 其他 进入 其他 行业备案首页
        self.driver.click(self.QiTa)
        
    def click_GongZhang(self):  #点击 公章刻制业 进入 公章刻制业 行业备案首页
        self.driver.click(self.GongZhang)
        
    def click_YuLe(self):  #点击 公共娱乐服务场所 进入 公共娱乐服务场所 行业备案首页
        self.driver.click(self.YuLe)
        
    def click_LvGuan(self):  #点击 旅馆业 进入 旅馆业 行业备案首页
        self.driver.click(self.LvGuan)
        
    def click_KaiSuo(self):  #点击 开锁业 进入 开锁业 行业备案首页
        self.driver.click(self.KaiSuo)
        
    def click_BaoAn(self):  #点击 保安服务业 进入 保安服务业 行业备案首页
        self.driver.click(self.BaoAn)
        
    def click_YinShua(self):  #点击 印刷业 进入 印刷业 行业备案首页
        self.driver.click(self.YinShua)
        
    def click_SheBao(self):  #点击 涉爆企业 进入 涉爆企业 行业备案首页
        self.driver.click(self.SheBao)
        
    def click_DianDang(self):  #点击 典当业 进入 典当业 行业备案首页
        self.driver.click(self.DianDang)
        
    def click_ZhongDian(self):  #点击 重点单位 进入 重点单位 行业备案首页
        self.driver.click(self.ZhongDian)
        
    def click_QiCheZuLin(self):  #点击 汽车租赁业 进入 汽车租赁业 行业备案首页
        self.driver.click(self.QiCheZuLin)
        
        
        

