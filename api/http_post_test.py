#-*- coding:utf-8 -*-
'''
Created on 2018年11月6日
@author: zhilh
Description: 
'''

from framework.Execl import ExcelUtil
from framework import log
import getcwd

import os
import unittest 
import ddt 
import requests
import json

 
    
@ddt.ddt
class TestSuite(unittest.TestCase):
    #装载测试数据
    execlName=os.path.join(getcwd.get_cwd(),"data\\PostTestCase.xlsx")
    caseData_excel = ExcelUtil(execlName, 'Sheet1')
    log.info('装载测试数据成功')
    
    @classmethod
    def setUpClass(cls):
        log.info('http-post接口测试:  http://honlp.angliancd.com:2358/semantic')

    @classmethod
    def tearDownClass(cls):
        log.info (u'接口测试结束')
        
    def setUp(self):
        print('case_id: ',self.id(),'开始执行<br />') #固定格式，用于报表生成

    def tearDown(self):
        print('结束执行<br />')#固定格式，用于报表生成
        
    def test_01(self):
        print('test_01')
        self.assertEqual('pass','pass','pass') 

    def test_02(self):
        print('test_02')
        self.assertEqual('pass','fail','fail') 

    @ddt.data(*caseData_excel.next())
    def test_case(self,data_):
        #接收数据
        text_ = str(data_['text'])
        intent_= str(data_['intent'])
        movie_name_= str(data_['movie_name'])
        movie_category_= str(data_['movie_category'])
        movie_actor_director_= str(data_['movie_actor_director'])
        movie_season_= str(data_['movie_season'])
        movie_episodes_= str(data_['movie_episodes'])
        song_category_= str(data_['song_category'])
        song_name_= str(data_['song_name'])
        song_singer_= str(data_['song_singer'])
        
        #数据整理，将测试数据中数字进行转换  2.0 -> 2
        if len(movie_season_)>0 and movie_season_.find('.') >0:
            movie_season_=movie_season_[0:movie_season_.find('.')]
        if len(movie_episodes_)>0 and movie_episodes_.find('.') >0:
            movie_episodes_=movie_episodes_[0:movie_episodes_.find('.')]
        
        #调用接口
        print(text_,' 开始测试') 
        post_data={'appkey':'yousibo389793@567~7','action':'semantic','text':''+text_+''}
        post_data=json.dumps(post_data)
        post_url='http://honlp.angliancd.com:2358/semantic'
        header={"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        r = requests.post(post_url,post_data,headers=header) 
        json_data = r.json()
        #print(type(r.json_data()),r.json_data())
        print('接口返回结果：',json_data)
        
        #根据接口定义，取出json格式数据中用于断言的信息
        json_str = 'intent-' + str(json_data['semantic']["intent"]) + '-'        
        for slots in json_data['semantic']['slots']:
            json_str = json_str + str(slots['name']) + '-' + str(slots['value']) + '-'
        #print('\n格式化后的字符串：',json_str)
                    
        #断言
        ifStr='(1==1'
        if len(intent_) > 0 :
            ifStr=ifStr+' and json_str.find("intent-'+intent_+'") != -1'
        if len(movie_name_) > 0 :
            ifStr=ifStr+' and json_str.find("movieName-'+movie_name_+'") != -1'
        if len(movie_category_) > 0 :
            ifStr=ifStr+' and json_str.find("movieCategory-'+movie_category_+'") != -1'
        if len(movie_actor_director_) > 0 :
            ifStr=ifStr+' and (json_str.find("actor-'+movie_actor_director_+'") != -1'
            ifStr=ifStr+' or json_str.find("director-'+movie_actor_director_+'") != -1'
            ifStr=ifStr+' or json_str.find("actor_director-'+movie_actor_director_+'") != -1)'
        if len(movie_season_) > 0 :
            ifStr=ifStr+' and json_str.find("movieSeason-'+movie_season_+'") != -1'
        if len(movie_episodes_) > 0 :
            ifStr=ifStr+' and json_str.find("movieEpisodes-'+movie_episodes_+'") != -1'
        ifStr=ifStr+')'
        
        #print('\n断言规则：',ifStr)
        if eval(ifStr) :
            print("测试结果：","pass")
            self.assertEqual('pass','pass','测试通过')
        else:
            print("测试结果：","fail")
            self.assertEqual('pass','fail','测试失败') 
    

if __name__ == "__main__":
    unittest.main()
   
   
   
           
        
