#coding=utf-8
import os
import threading
class DosCmd:
    def excute_cmd_result(self,command):
        result_list = []
        result = os.popen(command).readlines()
        for i in result:
            if i =='\n':
                continue
            result_list.append(i.strip('\n'))
            return result_list
    
    def excute_cmd(self,command):
        os.system(command)

class Port:
   def port_is_used(self,port_num):
      '''
      判断端口是否被占用
      '''
      flag = None
      self.dos = DosCmd()
      command = 'netstat -ano | findstr '+str(port_num)
      print(command)
      result = self.dos.excute_cmd_result(command)
      if len(result)>0:
         flag = True
      else:
         flag = False
      return flag

   def create_port_list(self,start_port,device_list):
      '''start_port 4701
      生成可用端口
      @parameter start_port
      @parameter device_list
      '''
      port_list = []
      if device_list != None:
         while len(port_list) != len(device_list):
            if self.port_is_used(start_port) != True:
               port_list.append(start_port)
            start_port = start_port +1
         return port_list
      else:
         print ("生成可用端口失败")
         return None
     
class Server:
    def get_devices(self):

        self.dos =DosCmd()
        devices_list = []
        result_list = self.dos.excute_cmd_result('adb devices')
        if len(result_list)>=2:
            for i in result_list:
                if 'List' in i:
                    continue
                devices_info = i.split('\t')
                if devices_info[1]=='device':
                 devices_list.append(devices_info[0])
            return devices_list
        else:
            return None
    def create_port_list(self,start_port):
        port=Port()
        port_list=port.create_port_list(start_port,self.get_devices())
        return  port_list
    def create_commed_list(self):
        command_list=[]
        appium_port_list=self.create_port_list(4700)
        bootstrap_port_list=self.create_port_list(4900)
        device_list=self.get_devices()
        for i in range(len(device_list)):
            command='appium -p '+str(appium_port_list[i])+" -bp "+str(bootstrap_port_list[i])+" -U "+device_list[i]+" --no-reset --session-override"
            command_list.append(command)
        return command_list
    def start_server(self,i):
        self.start_list=self.create_commed_list()
        self.dos.excute_cmd(self.start_list[i])
    def main(self):
        for i in range(len(self.create_commed_list())):
            appium_start=threading.Thread(target=self.start_server,args=(i,))
            appium_start.start()
            
                      
if __name__ == '__main__':
    #dos = DosCmd()
    #print (dos.excute_cmd_result('adb devices'))
    #port = Port()
    #li = [1,2,3,4,5]
    #print (port.create_port_list(4722,li))    
    server=Server()
    # print(server.create_commed_list())
    # print(server.start_server())
    print(server.main())
    