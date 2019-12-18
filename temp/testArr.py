#-*- coding:utf-8 -*-
'''
Created on 2018年11月8日
@author: zhilh
Description: 生成数组 
'''

def genMatrix(rows,cols):
    matrix = [[0 for col in range(cols)] for row in range(rows)]
    return matrix

def testlist():
    r,c=0,4
    lists=genMatrix(r,c)
    print(lists)
    for i in range(r):
        for j in range(c):
            print (i,j,': '+str(lists[i][j]))



"""
根据table的id属性和table中的某一个元素定位其在table中的位置
table包括表头，位置坐标都是从1开始算
tableId：table的id属性
queryContent：需要确定位置的内容
"""
def get_table_content(tableId,queryContent):
 
    # 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
    table_tr_list = driver.find_element(By.ID, tableId).find_elements(By.TAG_NAME, "tr")
    table_list = []  #存放table数据
    for tr in table_tr_list:    #遍历每一个tr
        #将每一个tr的数据根据td查询出来，返回结果为list对象
        table_td_list = tr.find_elements(By.TAG_NAME, "td")
        row_list = []
        print(table_td_list)
        for td in table_td_list:    #遍历每一个td
            row_list.append(td.text)    #取出表格的数据，并放入行列表里
        table_list.append(row_list)
 
    # 循环遍历table数据，确定查询数据的位置
    for i in range(len(table_list)):
        for j in range(len(table_list[i])):
            if queryContent== table_list[i][j]:
                print("%r坐标为(%r,%r)" %(queryContent,i+1,j+1))

list2d = [[1,2,3],[4,5,6]]
sum = 0
for i in  range(len(list2d)):
    for j in range(len(list2d[i])):
        if j ==0:
            sum = sum + list2d[i][j]
            print(list2d[i][j])
print(sum)
