#-*- coding:utf-8 -*-
'''
Created on 2018年10月13日
@author: zhilh
Description: 局域网共享文件夹下文件copy
    srcFilename: 源文件，若没有找到，系统返回提示信息 
    desFilename: 本地存放目录文件夹，若没有找到，系统会返回提示信息，并创建这个目录文件夹

'''

import os,sys 
from datetime import datetime  
  
def copyFileDir(srcFilename , desFilename):  
    status = False  
    try:  
        fileList = os.listdir(srcFilename)  
        for eachFile in fileList:  
            sourceF = os.path.join(srcFilename,eachFile)  
            targetF = os.path.join(desFilename,eachFile)  
  
            if os.path.isdir(sourceF):  
                if not os.path.exists(targetF):  
                    os.makedirs(targetF)  
                status = copyFileDir(sourceF,targetF)  
            else :  
                status = copyFile(sourceF,targetF)  
    except Exception as e:  
        print (e)  
        status = False  
    finally:  
        print ('copyFileDir function is quit!')  
    return status  
  
def copyFile(srcFilename , desFilename):  
    status = False  
    copyCommand = 'copy %s %s'%(srcFilename,desFilename)  
  
    try:  
        if(os.popen(copyCommand)):  #不用op.system(copyCommand),因为这个会弹出命令行界面  
            print ('copy done!')  
            status = True  
        else :  
            print ('copy failed!')  
            status = False  
    except Exception as e:  
        print (e)  
        status = False  
    finally:  
        print ('copyFile function is quit!')  
    return status  
  
def copyFromSharePath(srcFilename,desFilename):  
    if not os.path.exists(srcFilename):  
        print ('no found '+srcFilename)  
        return False  
    if not os.path.exists(desFilename):  
        print ('no found '+desFilename)  
        os.makedirs(str(desFilename))  
        print ('create '+desFilename)  
  
    copyStatus = False  
    if os.path.isdir(srcFilename):  
        copyStatus = copyFileDir(srcFilename,desFilename)  
    else :  
        copyStatus = copyFile(srcFilename,desFilename)  
    return copyStatus  
  
  
def runCopy(argv = sys.argv):  
    if not len(argv) == 2:  
        print ('input parameters\'s count should be 2,not %s'%(len(argv)))  
        return  
    srcFilename = argv[0]  
    #print (u'源目录：' + argv[0])  
    desFilename = argv[1]  
    #print (u'目标目录：' + argv[1])  
  
    if os.path.isdir(srcFilename):  
        if os.path.isfile(desFilename):  
            print ('can not copy a folder to a file')  
            return  
    copyFromSharePath(srcFilename,desFilename)  

def test():    
    import getcwd

    srcFilename = 'D:\\work\\昆山\\WHCS_12_05_01.apk'  
    desFilename = os.path.join(getcwd.get_cwd(),"download")  
      
    cmd = [  
        srcFilename,  
        desFilename  
    ]
    print(cmd)
    runCopy(cmd) 

   
if __name__=='__main__':  
    test()
    print('ok')
    
