#-*- coding:utf-8 -*-
'''
Created on 2018年8月29日
@author: zhilh

函数说明：send_mail() 函数实现发送带有多个附件的邮件，可以群发，附件格式包括：xlsx,pdf,txt,jpg,mp3,rar,html,png等
参数说明：
    1. subject：邮件主题
    2. content：邮件正文
    3. file_path：附件的地址, 输入格式为["D:\\test\\test.xlsx","E:\\temp\\tmp.jpg",...]
    4. receive_email：收件人地址, 输入格式为["25855192@qq.com","qq25855192@163.com",...]

'''

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.header import Header
import smtplib 
import os
from framework.readConfig import ReadConfig
from framework import  log
import getcwd

cf=ReadConfig()

class SendEmail:
    '''SMTP协议 发送邮件'''
    # 初始化基本信息，账号信息
    def __init__(self):
        self.mail_host = cf.get_config("EMAIL", "mail_host")
        self.mail_user = cf.get_config("EMAIL", "mail_user")
        self.mail_pass = cf.get_config("EMAIL", "mail_pass")
        self.mail_port = cf.get_config("EMAIL", "mail_port")
        self.from_ = cf.get_config("EMAIL", 'from')
        self.receiver = cf.get_config("EMAIL", 'receiver')
        self.subject = cf.get_config("EMAIL", "subject")
        self.content = cf.get_config("EMAIL", "content")
        self.logo_image = cf.get_config("EMAIL", "logo_image")
        self.on_off = cf.get_config("EMAIL", "on_off")
        self.me = self.mail_user.split("@")[0] + "<" + self.mail_user + ">" 
        self.server = smtplib.SMTP(self.mail_host, port=self.mail_port) 
        self.server.login(self.mail_user,self.mail_pass)
        self.logo_image=os.path.join(getcwd.get_cwd(),self.logo_image)
        #print(self.mail_host,self.mail_user,self.mail_pass,self.mail_port,self.receiver)    
      
    def send_mail(self, receive_email=None, subject=None, content=None, files=None,images=None,subtype='html'):        
        #如果发送的是文本邮件，则subtype设置为plain
        #如果发送的是html邮件，则subtype设置为html
        if receive_email==None:
            receive_email = self.receiver
        if subject==None:
            subject = self.subject
        if content==None:
            content = self.content
        if files==None:
            files = []            
        if images==None:
            images =self.logo_image
            if len(images) > 0:
                images=images.split(',')

        if self.on_off != '1':
            log.info('系统设置不发送邮件')
            return
             

        # 创建邮件结构
        msg = MIMEMultipart()  
        msg['Subject'] = Header(subject,'utf-8')  
        msg['From'] = Header(self.from_,'utf-8')
        msg['To'] = ",".join(receive_email.split(','))
        
        #添加附件，若没有找到这个附件则继续找下一个附件
        for path in files:
            path = path.replace("/","//")
            path = path.replace("\\","//")
            if not os.path.exists(path):  
                log.info ('没有找到附件 '+path)  
                #return False    #结束发送邮件
                #break   #退出循环继续发送邮件
                continue    #退出单次循环继续查找其他附件
            file_name = path.split("//")[-1]
            part = MIMEApplication(open(path,'rb').read()) 
            part.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(part)
            
        #添加邮件正文中需要显示的图片
        #图片id加入所在位置
        content=content+'<br><br><br><br><br><br>'
        for index in range(len(images)):
            if index % 2 == 0:
                content += '<img src="cid:'+str(index)+'"><br>'
            else:
                content += '<img src="cid:' + str(index) + '">'                        
        #将图片和id位置对应起来
        index=0
        for img_path in images:
            img_path = img_path.replace("/","//")
            img_path = img_path.replace("\\","//")
            if not os.path.exists(img_path):  
                log.info ('没有找到图片 '+img_path)  
                continue
            msgImage = MIMEImage(open(img_path, 'rb').read())
            msgImage.add_header('Content-ID', '<'+str(index)+'>')
            index += 1
            msg.attach(msgImage)
        
        #增加邮件正文
        #log.info(content)
        msg.attach(MIMEText(content, _subtype=subtype, _charset="utf-8"))
                    
        try:
            self.server.sendmail(self.me, msg['To'].split(','), msg.as_string())   
            #self.server.sendmail('qq25855192@163.com',' lianghua.zhi@vdin.net', msg.as_string()) 
            log.info('邮件发送成功') 
        except Exception as e:  
            print(e)
            log.info('邮件发送失败')
    
    # 释放资源  
    def __del__(self):
        try:
            if not self.is_closed:
                self.server.quit()
                self.close()
        except AttributeError:
            pass
       

def test_sendMail():
    mail=SendEmail()
    print(mail)
    mail.send_mail(
        files=['D:\\Python\\eclipse-workspace\\WebPublic\\report\\20180930-142938-result.html','D:\\Python\\eclipse-workspace\\WebPublic\\report\\20180930-152722-result.html'],
        images=['D:\Python\eclipse-workspace\WebPublic\data\logo_vdin.png','D:\Python\eclipse-workspace\WebPublic\data\pawge.png']
        )
    #mail.send_mail()
    
if __name__ == '__main__':
    pass
    #test_sendMail()
    

    
