#-*- coding:utf-8 -*-
'''
Created on 2019年10月15日
@author: zhilh
Description: 接口测试--接口功能测试
    测试用例由execl提供，测试结果回写到execl
'''

import unittest,os
from framework.Bases import PySelenium
from framework import log
from framework.func import testPass
from framework import rdData


import ddt
from framework.Execl import ExcelUtil,ExcelAdd
import getcwd


@ddt.ddt
class api_detect(unittest.TestCase):
    '''人脸识别'''
    #装载测试数据
    execlName=os.path.join(getcwd.get_cwd(),"data\\api_data_detect.xls")
    caseData_excel = ExcelUtil(execlName, 'Sheet1')
    writer_table=ExcelAdd(execlName,sheet='Sheet1')
    log.info('装载测试数据成功')
    col_Num=writer_table.get_cols()
    writer_table.modify_cell(0, writer_table.get_cols(), 'status')
    writer_table.modify_cell(0, writer_table.get_cols()+1, 'return_msg')
    log.info('Execl文件表头写入成功')

    @classmethod
    def setUpClass(self):
        log.info('开始测试...')
    
    @classmethod
    def tearDownClass(self):
        self.writer_table.save()#保存execl测试结果
        #self.dr.quit()  #关闭浏览器
        log.info('测试完成，退出系统，关闭浏览器')
    
    def setUp(self):        
        print('case_id: ',self.id(),'开始执行<br />') #固定格式，用于报表生成        
             
    def tearDown(self):
        '''测试报错或者用例不通过则截图'''
        if not testPass(self):
            print('截图: img\\report_img.png <br />')#固定格式，用于报表生成
        print('结束执行<br />')#固定格式，用于报表生成

    @ddt.data(*caseData_excel.next())  
    def test_index(self,test_data):
     
        place_dict={
            'cur_row':test_data['curRow'],#当前execl数据表数据行
            'place_name':test_data['place_name'].strip(), #企业名称
            'industry_name':test_data['industry_name'].strip(), #所属行业
            'person_name':test_data['person_name'].strip(), #法人姓名
            'person_phone':test_data['person_phone'].strip(), #法人电话号码           
            }
        print('备案信息：',place_dict)            
        
        
        '''第一页 选择行业'''
        self.page=placeIndex(self.dr) #企业备案引导首页 元素
        self.assertEqual('新增企业备案' ,self.page.get_page_title(),'页面标题不一致')
        self.page.select_industry(place_dict['industry_name'])
         

        #断言
        if self.page.place_success_name_is_enabled():
            self.assertTrue(1==1,'企业备案成功')
            self.writer_table.modify_cell(place_dict['cur_row'], writer_table.get_cols(),globals()['node_name'])
            self.writer_table.modify_cell(place_dict['cur_row'], writer_table.get_cols()+1,'备案成功')
            log.info("企业备案成功:%s,%s,%s,%s" %(globals()['node_name'],globals()['login_name'],place_dict['industry_name'],place_dict['place_name']))
        else:
            self.assertTrue(1==2,'企业备案失败')
        
        
if __name__ == '__main__':
    unittest.main()



