#-*- coding:utf-8 -*-
'''
Created on 2019年12月31日
@author: zhilh
Description: 
'''
from framework.ssh import SSHhandle
 
def main():
    sh = SSHhandle('192.168.100.217')
    sh.connect()
    ret = sh.exc_cmd('ls -l /opt',)
    print('The cmd excute result is :%s' % ret)
    sh.sftp_put('test.txt', '/opt/text')
    sh.close()
 
if __name__ == '__main__':
    main()
