#-*- coding:utf-8 -*-
'''

Created on 2018年9月21日

@author: zhilh

'''
import xlrd

class ExcelUtil(object):  
    '''unittest框架的基于execl格式的ddt数据驱动'''  
    def __init__(self, excelPath, sheetName):  
        self.data = xlrd.open_workbook(excelPath)  
        self.table = self.data.sheet_by_name(sheetName)  
          
        #get titles  
        self.row = self.table.row_values(0)  
          
        #get rows number  
        self.rowNum = self.table.nrows  
          
        #get columns number  
        self.colNum = self.table.ncols  
          
        #the current column  
        self.curRowNo = 1  
          
    def next(self):  
        r = []  
        while self.hasNext():  
            s = {}  
            col = self.table.row_values(self.curRowNo)  
            i = self.colNum  
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

