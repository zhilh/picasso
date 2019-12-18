#-*- coding:utf-8 -*-
'''
Created on 2019年1月29日
@author: zhilh
Description: 网约房爬虫数据坐标验证
'''

import os
import unittest
from framework.Bases import PySelenium
from framework import log
from framework.Execl import ExcelUtil,ExcelAdd
from framework import func

import ddt
import getcwd

    
@ddt.ddt
class TestSuite(unittest.TestCase):
    #装载测试数据
    execlName=os.path.join(getcwd.get_cwd(),"data\\spider_house.xls")
    caseData_excel = ExcelUtil(execlName, 'spider_house')
    #打开execl文件
    writer_table=ExcelAdd(execlName,sheet='spider_house')
    col_Num=writer_table.get_cols()
    #写入表头
    writer_table.modify_cell(0, col_Num, 'gd_lon')
    writer_table.modify_cell(0, col_Num+1, 'gd_lat')
    writer_table.modify_cell(0, col_Num+2, 'distance')
    log.info('装载测试数据成功')
    
    @classmethod
    def setUpClass(self):
        self.dr = PySelenium()
        self.dr.openUrl('https://lbs.amap.com/console/show/picker')
        log.info('网约房爬虫数据坐标验证，以高德地图api查询结果为标准')

    @classmethod
    def tearDownClass(self):
        self.writer_table.save()#保存测试结果
        self.dr.quit()  #关闭浏览器
        log.info ('测试结束，关闭浏览器')
        
    def setUp(self):
        print('case_id: ',self.id(),'开始执行<br />') #固定格式，用于报表生成
        self.dr.F5()

    def tearDown(self):
        '''测试报错或者用例不通过则截图'''
        if not func.testPass(self):
            print('截图: ',self.dr.getScreenshot( self.id()),'<br />')#固定格式，用于报表生成
        print('结束执行<br />')#固定格式，用于报表生成
        
    @ddt.data(*caseData_excel.next())
    def test_case(self,data_):
        #接收测试数据
        cur_row=data_['curRow']
        lon = str(data_['lon'])
        lat= str(data_['lat'])
        address= str(data_['address'])
        
        #页面元素封装
        txtSearch='id=>txtSearch'
        btnSearch='class=>btn-search'
        #divCoordinate='id=>divCoordinate'
        picker_copy='class=>picker-copy'
        
        #模拟查询操作
        self.dr.inputText(txtSearch, address)
        #self.dr.clear(id_Coordinate)
        self.dr.click(btnSearch)
        self.dr.waitSleep(2)
        self.dr.click(picker_copy)
        coordinate = str(func.get_clipBoard_text())
        func.set_clipBoard_text("b'0,0'")
        #coordinate=self.dr.getText(divCoordinate)
        gd_lon=coordinate[coordinate.find("'")+1:coordinate.find(",")]
        gd_lat=coordinate[coordinate.find(",")+1:len(coordinate)-1]
        #print(lat, lon, gd_lat, gd_lon)
        distance=func.get_distance_hav(float(lat), float(lon), float(gd_lat), float(gd_lon)) * 1000

        #断言，写入数据到execl文件        
        self.writer_table.modify_cell(cur_row, self.col_Num,gd_lon)
        self.writer_table.modify_cell(cur_row, self.col_Num+1, gd_lat)
        self.writer_table.modify_cell(cur_row, self.col_Num+2, distance)
        

if __name__ == "__main__":
    unittest.main()
   
   
   
           
        
