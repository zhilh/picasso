#-*- coding:utf-8 -*-
'''
Created on 2019年12月31日
@author: zhilh
Description: 
    封装简单ssh命令操作方法
'''

import paramiko

 
 
class SSHhandle(object):
 
    def __init__(self, host, port=22, username='root', password='password'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
 
    def connect(self):
        transport = paramiko.Transport(self.host, self.port)
        transport.connect(username=self.username, password=self.password)
        self.__transport = transport
 
    def close(self):
        self.__transport.close()
 
    def exc_cmd(self, cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh._transport = self.__transport  # 巧妙的使用了ssh的私有属性
        stdin, stdout, stderr = ssh.exec_command(cmd)
        #print('the excute cmd is: %s' %cmd) 
        return stdin, stdout, stderr
 
    def sftp_put(self, localpath, remotepath):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(localpath, remotepath)


