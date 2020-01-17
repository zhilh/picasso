#-*- coding:utf-8 -*-
'''

Created on 2018年9月25日

@author: 

'''

import os
import xlrd
from xlutils.copy import copy


class ExcelUtil(object):  
    '''unittest框架的基于execl格式的ddt数据驱动'''  
    def __init__(self, excelPath, sheetName):  
        self.data = xlrd.open_workbook(excelPath)  
        self.table = self.data.sheet_by_name(sheetName)            
        #表头、标题  
        self.row = self.table.row_values(0)            
        #总行数 
        self.rowNum = self.table.nrows            
        #总列数  
        self.colNum = self.table.ncols            
        #当前列  
        self.curRowNo = 1  
          
    def next(self):  
        r = []  
        while self.hasNext():  
            s = {}  
            col = self.table.row_values(self.curRowNo)  
            i = self.colNum  
            s['curRow']= self.curRowNo #存放当前行数
            for x in range(i):  
                s[self.row[x]] = col[x] 
            r.append(s)  
            self.curRowNo += 1  
        return r         
      
    def hasNext(self):  
        if self.rowNum == 0 or self.rowNum <= self.curRowNo :  
            return False  
        else:  
            return True 


class ExcelReader:
    """
    读取excel文件中的内容。返回list。
    如：
    excel中内容为：
    | A  | B  | C  |
    | A1 | B1 | C1 |
    | A2 | B2 | C2 |
    如果 print(ExcelReader(excel, title_line=True).data)，输出结果：
    [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]
    如果 print(ExcelReader(excel, title_line=False).data)，输出结果：
    [[A,B,C], [A1,B1,C1], [A2,B2,C2]]
    可以指定sheet，通过index或者name：
    ExcelReader(excel, sheet=2)
    ExcelReader(excel, sheet='TestData')
    """
    def __init__(self, excel, sheet=0, title_line=True):
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()
 
    @property
    def data(self):
        if not self._data:
            workbook = xlrd.open_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise TypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)
 
            if self.title_line:
                title = s.row_values(0)  # 首行为title
                for col in range(1, s.nrows):
                    # 依次遍历其余行，与首行组成dict，拼到self._data中
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                for col in range(0, s.nrows):
                    # 遍历所有行，拼到self._data中
                    self._data.append(s.row_values(col))
        return self._data
 
 
class ExcelAdd:
    """
    向已存在excel文件中写入内容
    """
    def __init__(self, excel, sheet=0):
        """
        :param excel: 文件地址
        :param sheet: 选定sheet  默认为：0
        """
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet
        
        r_xls = xlrd.open_workbook(self.excel,formatting_info=True)    #formatting_info 保留格式打开，只支持xls格式
        if type(self.sheet) not in [int, str]:
            raise TypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
        elif type(self.sheet) == int:
            r_sheet = r_xls.sheet_by_index(self.sheet)
        else:
            r_sheet = r_xls.sheet_by_name(self.sheet)
        self.rows = r_sheet.nrows
        self.cols = r_sheet.ncols        
        self.w_xls = copy(r_xls)
        self.sheet_write = self.w_xls.get_sheet(self.sheet)        
    
    def get_rows(self):
        '''
        总行数
        '''
        return self.rows
        
    def get_cols(self):
        '''
        总列数
        '''
        return self.cols

    def save(self,file_name=None):
        fpath,fname=os.path.split(self.excel)   #分离文件名和路径
        new_execl=fpath+'//ret_'+fname  #重命名
        if file_name != None:
            new_execl=fpath+'//'+file_name  #自定义名称
        self.w_xls.save(new_execl)
        return new_execl
    
    def modify_cell(self, row=0, col=0, data=""):
        """
        修改一个单元格的数据（覆盖原数据）
        :param row: 行
        :param col: 列
        :param data: 数据
        :return:
        """
        self.sheet_write.write(row, col, data)
      
    def add_rows(self,values):
        '''
        增加多行数据
        values=(('a','b','as','de','fg',...),(...))
        '''
        for i in values :
            k=0
            for j in i:
                self.sheet_write.write(self.rows, k, j)
                k=k+1
            self.rows=self.rows+1   #增加一行后，总行数增加一
    
    def add_cols(self,values):
        '''
        增加多列数据
        values=(('a','b','as','de','fg',...),(...))
        '''
        for i in values :
            k=0
            for j in i:
                self.sheet_write.write( k,self.cols, j)
                k=k+1
            self.cols=self.cols+1   #增加一列后，总列数增加一
 
def testR(e):    
    reader = ExcelReader(e, sheet=0,title_line=False)
    data_table=reader.data
    print(len(data_table))  #行数
    print(len(data_table[0]))   #列数
    for i in range(0,len(data_table)):
        print(data_table[i])
     
def testW(e):    
    row = 1
    col = 0
    data = '数据库2'
    writer_table=ExcelAdd(e,sheet=0)
    writer_table.modify_cell( 10, col, data)#修改指定的单元格数据
    print(writer_table.get_cols(),writer_table.get_rows())
    
    row_data=[('11', '拆迁', '', '邛崃', '全部', '全部', '全部1'),('12', '拆迁', '', '高新区', '全部', '全部2'),('13', '旅馆', '', '武侯区', '全部3')]
    writer_table.add_rows(row_data)#增加多行数据
    
    row_data=[('15', '酒店', '', '', '全部', '全部', '全部')]
    writer_table.add_rows(row_data)#增加一行数据
    
    col_data=('测试结果', '通过', '通过', '通过', '通过', '通过', '通过', '通过', '通过','通过','通过'),
    writer_table.add_cols(col_data)#增加一列数据
    
    col_data=(('检查结果', '通过', '通过', '通过', '通过', '通过', '通过'), ('备注', '这条case需要多测试几次','数据项复测','核对结果不准确'))
    writer_table.add_cols(col_data)#增加多列数据
    
    return writer_table.save()#保存为新的execl文件
    
if __name__ == "__main__":
    pass
    xls= r'..//data//test.xls'
    #f=testW(xls)    
    testR(xls)
 
    
    
