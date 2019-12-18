#-*- coding:utf-8 -*-
'''

Created on 2018年9月13日

@author: zhilh

'''
import pytesseract
from PIL import Image
from PIL import ImageEnhance


class getVerifyCode(object):
    def __init__(self):
        # 二值化  
        self.threshold = 140  
        self.table = []  
        for i in range(256):  
            if i < self.threshold:  
                self.table.append(0)  
            else:  
                self.table.append(1)  
          
        #由于都是数字，对于识别成字母的 采用该表进行修正  
        self.rep={
            'O':'0', 'D':'0','Q':'0', 
            'I':'1','L':'1',  
            'Z':'2',  
            'T':'7','%':'7',  
            'B':'8','S':'8','$':'8',
            'G':'6'  
            };  
        
    def getCode(self,img_path,img_name):
        im = Image.open(img_path+img_name)  #打开图片      
        imgry = im.convert('L')#转化到灰度图        
        imgry = ImageEnhance.Contrast(imgry)  # 对比度增强
        imgry = imgry.enhance(2.0)
        imgry.save(img_path+'g'+img_name)  #保存图像
        
        #二值化，采用阈值分割法，threshold为分割点 
        out = imgry.point(self.table,'1')  
        out.save(img_path+'b'+img_name)  
        text = pytesseract.image_to_string(out)  #识别  
        #修正 
        text = text.strip().replace(' ','')  
        text = text.upper()
        for r in self.rep:  
            text = text.replace(r,self.rep[r])   
        #out.save(text+'.jpg')  
        #print (text)  
        return text        
        
if __name__ == '__main__':
    imgcode= getVerifyCode()
    code=imgcode.getCode('..//data//','test.png')       
  
        
        
        
        
        
        
        