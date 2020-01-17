#-*- coding:utf-8 -*-
'''
Created on 2019年12月26日
@author: zhilh
Description: 
'''


'''
xlsread_info()     获取表的信息     返回表的行和列
xlsread_data()     获取表的所有数据     返回list
xlsread_allnrows()     通过行的方式或取表的所有数据     返回list
xlsread_allncols()     通过列的方式或取表的所有数据     返回list
xlsread_matching_title(matching_value，nrows_number)     匹配value所在的列的第几行数据     返回string
xlsread_matching_data(matching_value)     匹配value所在表中的所有位置     返回list
xlsred(nrows_number,ncols_number)     读取指定位置的数据     返回string
excelwrite(data,nrows_number,ncols_number)     在指定位置写入数据并新建该excel文件     返回在表中最后操作位置
nrows_write(data_list,nrows_number )     对指定行写入数据并新建该excel文件     返回在表中最后操作位置
ncols_write(data_list,ncols_number)     对指定列写入数据并新建该excel文件     返回在表中最后操作位置
dict_write(data_dict)     对字典数据写入数据并新建该excel文件     返回在表中最后操作位置
add_nrows(data,ncols_number)     从excel最后一行的下面空白行增加一行数据，从第指定列开始增加     返回在表中最后操作位置
add_ncols(data,nrows_number)     从excel最后一列的后面空白列增加一行数据，从第指定行开始增加     返回在表中最后操作位置
add_dict(data,methods=“nrows\ncols”,start_number)     将字典数据增加在最后一行或者列后面面空白行或列；methods = nrows 每行开始增加；methods = ncols 每列开始增加     返回在表中最后操作位置
change_data(new_data,nrows_number,ncols_number)     更改某位置的值     返回在表中最后操作位置
replace_data(data,new_data)     将excel中所有data跟换成new_data     返回更改数据数量
replace_nrows(data,nrows_number)     替换指定行的数据     返回更改数据数量
replace_ncols(data,ncols_number)     替换指定行的数据     返回更改数据数量
del_alldata()     清空excel上的内容     返回清空数据数量
del_nrows(nrows_number)     清空excel指定行的数据     返回清空数据数量
del_ncols(ncols_number)     清空excel指定列的数据     返回清空数据数量
del_data(nrows_number,ncols_number)     清空excel上指定位置的数据     返回在表中最后操作位置
del_value(data)     删除excel指定数据     返回清空数据数量
'''

import os
import sys
import xlrd
import xlwt
from xlutils.copy import copy
import json

#横坐标 字母与数字转换
def letter(nrows_number):
    #构造 A~Z  ： [chr(i) for i in range(65,91)]
    all_list=[chr(i) for i in range(65,91)]
    letter_list=[chr(i) for i in range(65,91)]
    #如果收到的收到的 nrows_number 是int类型，就要寻找对应字母。列： 1=A 27=AA
    if isinstance(nrows_number,int) is True:
        for first in letter_list:
            for second  in letter_list:
                all_list.append(first+second)
        #print all_list
        return all_list[nrows_number-1]
    #如果收到的收到的 nrows_number 是str类型，寻找字母对应第几个。列： A=1 AA=27
    elif isinstance(nrows_number,str) is True:
        nrows_number = nrows_number.upper()
        for first in letter_list:
            for second  in letter_list:
                all_list.append(first+second)
        if nrows_number in all_list:
            return all_list.index(nrows_number)+1
        else:
            return 'Input Error.'
    else:
        print('input int or string.')

class Excel_funtion:
    def __init__(self,excel_filename,sheet_name=''):
        self.excel_filename=excel_filename
        #存在两种模式：
        #1. 文件不存在，当文件不存在只能新建，初始操作只能为写; 为  mode=0
        #2. 文件存在,不能新建重名重位置的文件，能读写，增删改查; 为  mode=1
        #根据这个规则，友善规避错误的操作，不用每个函数功能都去try;
        if not os.path.exists(self.excel_filename):
            print ("not file "+self.excel_filename)
            self.mode = 0
            self.new_book = xlwt.Workbook(encoding='utf-8')#, style_compression=0)
            #style_compression:表示是否压缩，不常用。
            # cell_overwrite_ok，表示是否可以覆盖单元格，其实是Worksheet实例化的一个参数，默认值是False
            if sheet_name == '':
                self.sheet_name = "sheet"
                self.sheet = self.new_book.add_sheet(self.sheet_name,cell_overwrite_ok=True)
            else:
                self.sheet_name = sheet_name
                self.sheet = self.new_book.add_sheet(self.sheet_name,cell_overwrite_ok=True)
        else:
            print ("open file "+self.excel_filename)
            self.mode = 1
            self.book= xlrd.open_workbook(self.excel_filename)
            self.handle = copy(self.book)
            
            if sheet_name == '':
                self.sheet = self.book.sheet_by_index(0)
                self.sheet_name = "sheet"
                self.handle_sheet = self.handle.get_sheet(0)
            else:
                try:
                    self.sheet = self.book.sheet_by_name(sheet_name)
                    self.sheet_name = sheet_name
                    self.handle_sheet = self.handle.get_sheet(sheet_name)
                except:
                    print ("not "+sheet_name+" in "+ excel_filename)

    #excel info return info
    def xlsread_info(self):
        if self.mode == 1:
            print ("file: "+self.excel_filename)
            print ("sheet name: "+self.book.sheet_names()[0])
            nrows = self.sheet.nrows    # 获取行总数
            print ("nrows: ",nrows)
            ncols = self.sheet.ncols    #获取列总数
            print ("ncols: ",ncols)
            return nrows,ncols
        else:
            print(self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #data打印  return data
    def xlsread_data(self):
        if self.mode == 1:
            for i in range(self.sheet.nrows):
                return self.sheet.row_values(i)
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #每行打印 return data
    def xlsread_allnrows(self):
        if self.mode == 1:
            data_list=[]
            for i in range(self.sheet.nrows):
                data=[]
                for n in range(self.sheet.ncols):
                    if self.sheet.cell(i,n).value != '':
                        data.append(self.sheet.cell(i,n).value)
                data_list.append(data)
            return data_list
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #每列打印 return data
    def xlsread_allncols(self):
        if self.mode == 1:
            data_list=[]
            for i in range(self.sheet.ncols):
                data=[]
                for n in range(self.sheet.nrows):
                    if self.sheet.cell(n,i).value != '':
                        data.append(self.sheet.cell(n,i).value)
                data_list.append(data)
            return data_list
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #打印匹配列的数据 return data
    def xlsread_matching_title(self,matching_value,nrows_number=0):
        if self.mode == 1:
            data_list=[]
            for i in range(self.sheet.ncols):
                if self.sheet.cell(nrows_number,i).value == matching_value:
                    data=[]
                    for n in range(self.sheet.nrows):
                        if self.sheet.cell(n,i).value != '':
                            data.append(self.sheet.cell(n,i).value)
                    print ("title_name: ",matching_value)
                    print ("Data-ncols: ",i+1)
                    print ("Data-number: ",n)
                    print (data)
                    data_list.append(data)
            return data_list
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #查找是否存在对应数据，返回这个数据存在该表内所有的位置信息 return data
    def xlsread_matching_data(self,matching_value):
        if self.mode == 1:
            print ("fond data : ",matching_value)
            seat_list=[]
            for i in range(self.sheet.ncols):
                seat=[]
                for n in range(self.sheet.nrows):
                    if matching_value == self.sheet.cell(n,i).value:
                        seat_value=n,i
                        seat.append(seat_value)
                if seat != []:
                    seat_list.append(seat)     
            return seat_list
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #读取指定位置的数据 return data
    def xlsred(self,nrows_number,ncols_number):
        if self.mode == 1:
            str = self.sheet.cell(nrows_number,ncols_number).value
            print ("read data : ",str)
            print ("Data-ncols: ",nrows_number)
            print ("Data-number: ",ncols_number)
            return str
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #写操作 写入数据   return x,y
    def excelwrite(self,data,nrows_number,ncols_number):
        if self.mode == 0:
            self.sheet.row(nrows_number).write(ncols_number, data)
            self.new_book.save(self.excel_filename)
            return nrows_number+1,ncols_number+1
        else:
            print (self.excel_filename+u" 已存在,无法再次创建重名文件和写操作!!!")
            return 0,0

    #对指定行写入数据
    def nrows_write(self,data_list,nrows_number):
        if self.mode == 0:
            for i, item in enumerate(data_list):
                self.sheet.row(nrows_number).write(i, item)
            self.new_book.save(self.excel_filename)
            return letter(nrows_number),i+1
        else:
            print (self.excel_filename+u" 已存在,无法再次创建重名文件和写操作!!!")
            return 0,0

    #对指定列写入数据
    def ncols_write(self,data_list,ncols_number):
        if self.mode == 0:
            for i, item in enumerate(data_list):
                self.sheet.row(i).write(ncols_number, item)
            self.new_book.save(self.excel_filename)
            return letter(i+1),ncols_number+1
        else:
            print (self.excel_filename+u" 已存在,无法再次创建重名文件和写操作!!!")
            return 0,0

    #对字典进行数据写入
    def dict_write(self,data_dict):
        if self.mode == 0:
            #判断写入的数据类型是否为字典
            if type(data_dict).__name__ == 'dict':
                nrows_number=0
                ncols_number=0
                for key in data_dict:
                    #一行一行的写
                    self.sheet.row(nrows_number).write(ncols_number, key)
                    self.sheet.row(nrows_number).write(ncols_number+1, data_dict[key])
                    nrows_number+=1
                    ncols_number=0
                self.new_book.save(self.excel_filename)
                return nrows_number+1,letter(ncols_number+1)
            else:
                print ("data not is dict type.")
                return 0,0
        else:
            print (self.excel_filename+u" 已存在,无法再次创建重名文件和写操作!!!")
            return 0,0

    #利用 xlutils.copy 来实现增删改，缺点 速度相对于其他库较慢； 优点： 完全满足增删改功能
    #
    #增加数据， 找到最后一行进行增加一行数据，从第指定列开始增加
    def add_nrows(self,data,ncols_number):
        if self.mode == 1:
            #找到最后一行
            nrows_number = self.sheet.nrows
            for i, item in enumerate(data):
                self.handle_sheet.write(nrows_number,i+ncols_number,item)
            self.handle.save(self.excel_filename)
            return nrows_number+1,letter(i+ncols_number+1)
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #增加数据， 找到最后一列进行增加一列数据，从第指定行开始增加
    def add_ncols(self,data,nrows_number):
        if self.mode == 1:
            #找到最后一列
            ncols_number = self.sheet.ncols
            for i, item in enumerate(data):
                self.handle_sheet.write(nrows_number+i,ncols_number,item)
            self.handle.save(self.excel_filename)
            return nrows_number+i+1,letter(ncols_number+1)
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    # 增加数据， 最后位置行或列从指定开始位置增加字典数据
    # methods = nrows 每行开始增加
    # methods = ncols 每列开始增加
    def add_dict(self,data,methods="nrows",start_number=0):
        if self.mode == 1:
            #找到最后一行一列
            nrows_number = self.sheet.nrows
            ncols_number = self.sheet.ncols
            if type(data).__name__ == 'dict':
                if methods == "nrows":
                    ncols_start = start_number
                    for key in data:
                        self.handle_sheet.write(nrows_number,ncols_start, key)
                        self.handle_sheet.write(nrows_number,ncols_start+1, data[key])
                        nrows_number += 1
                        ncols_start = start_number
                    self.handle.save(self.excel_filename)
                    return nrows_number,letter(ncols_start+2)
                elif methods == "ncols":
                    nrows_start = start_number
                    for key in data:
                        self.handle_sheet.write(nrows_start,ncols_number, key)
                        self.handle_sheet.write(nrows_start+1,ncols_number, data[key])
                        ncols_number += 1
                        nrows_start = start_number
                    self.handle.save(self.excel_filename)
                    return nrows_start+2,letter(ncols_number)
                else:
                    print ("methods only be nrows or ncols.")
                    return nrows_number,letter(ncols_number+1)
            else:
                print ("data not is dict type.")
                return nrows_number,letter(ncols_number+1)
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #改某位置的值
    def change_data(self,data,nrows_number,ncols_number):
        if self.mode == 1:
            self.handle_sheet.write(nrows_number-1,ncols_number-1,data)
            self.handle.save(self.excel_filename)
            return nrows_number,letter(ncols_number)
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #替换到全表的某个值
    #首选找出这个值在表中的所有位置，再将其替换
    #返回被更改的数据个数
    def replace_data(self,data,new_data):
        if self.mode == 1:
            replace_number = 0
            for i in range(self.sheet.ncols):
                for n in range(self.sheet.nrows):
                    if data == self.sheet.cell(n,i).value:
                        self.handle_sheet.write(n,i,new_data)
                        replace_number += 1
            self.handle.save(self.excel_filename)
            return replace_number
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'
    
    #替换一行
    def replace_nrows(self,data,nrows_number):
        if self.mode == 1:
            for i, item in enumerate(data):
                    self.handle_sheet.write(nrows_number-1,i,item)
            self.handle.save(self.excel_filename)
            return nrows_number,letter(i+1)
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #替换一列    
    def replace_ncols(self,data,ncols_number):
        if self.mode == 1:
            for i, item in enumerate(data):
                    self.handle_sheet.write(i,ncols_number-1,item)
            self.handle.save(self.excel_filename)
            return i+1,letter(ncols_number)
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'
  
    #删除全部
    def del_alldata(self):
        if self.mode == 1:
            replace_number = 0
            for i in range(self.sheet.ncols):
                for n in range(self.sheet.nrows):
                    self.handle_sheet.write(n,i,'')
                    replace_number += 1
            self.handle.save(self.excel_filename)
            return replace_number
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #删除行
    def del_nrows(self,nrows_number):
        if self.mode == 1:
            replace_number = 0
            for i in range(self.sheet.ncols):
                self.handle_sheet.write(nrows_number-1,i,'')
                replace_number += 1
            self.handle.save(self.excel_filename)
            return replace_number
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #删除列
    def del_ncols(self,ncols_number):
        if self.mode == 1:
            replace_number = 0
            for n in range(self.sheet.nrows):
                self.handle_sheet.write(n,ncols_number-1,'')
                replace_number += 1
            self.handle.save(self.excel_filename)
            return replace_number
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #删除某个位置
    def del_data(self,nrows_number,ncols_number):
        if self.mode == 1:
            self.handle_sheet.write(nrows_number+1,ncols_number+1,'')
            self.handle.save(self.excel_filename)
            return self.sheet.cell(ncols_number+1,nrows_number+1).value
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'

    #删除指定数据
    def del_value(self,data):
        if self.mode == 1:
            replace_number = 0
            for i in range(self.sheet.ncols):
                for n in range(self.sheet.nrows):
                    if data == self.sheet.cell(n,i).value:
                        self.handle_sheet.write(n,i,'')
                        replace_number += 1
            self.handle.save(self.excel_filename)
            return replace_number
        else:
            print (self.excel_filename+u" 不存在,无法进行操作!!!")
            return 'error: not file.'




def test():
    
    #excelWrite()
    #add()
    #excelRead()

    exl=Excel_funtion('..//data//test.xls')
    
    x,y=exl.xlsread_info()
    #print(x,y)
        
    a_data="Liman"
    a_list=[1,2,3,4,5,6,'a','b']
    a_dict={'a': '1', 'b': '2', 'c': '3'}
    #print (exl.del_value('a'))
    #print letter(1)
    #print letter('a')

if __name__ == '__main__':
    test()