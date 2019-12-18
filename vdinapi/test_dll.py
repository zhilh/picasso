#-*- coding:utf-8 -*-
'''
Created on 2019年10月23日
@author: zhilh
Description: python调用dll动态库测试
'''

import ctypes
import sys,os
curPath = os.path.abspath(os.path.dirname(__file__))
projPath = os.path.split(curPath)[0]
sys.path.append(projPath)

dllPath=os.path.join(projPath,"dll\\OpencvTest\\OpencvMat.dll")
print (dllPath)
#mydll=ctypes.cdll.LoadLibrary(dllPath)
#print(mydll)
pDll=ctypes.CDLL("dllpath")
print (pDll)

#pResutl= pDll.sum(1,4)
#pResult2=pDll.sub(1,4)
#print (pResutl)
#print (pResult2)

