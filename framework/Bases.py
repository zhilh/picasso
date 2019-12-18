#-*- coding:utf-8 -*-
'''
Created on 2018年8月30日
@author: zhilh
Description: web端自动化基础操作封装
'''
import time,os

from PIL import Image

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

from framework.Screenshot import Screenshot
from framework.getVerifyCode import getVerifyCode
import getcwd


import win32api
import win32con



'''
    对selenium进行二次封装
'''
class PySelenium(object):
    '''
        初始化,实例化浏览器驱动对象
    '''
    def __init__(self, browser='chrome'):
        if browser == 'ff' or browser == 'firefox': # 火狐
            driver = webdriver.Firefox()
        elif browser == 'chrome': # 谷歌
            os.system('taskkill /im chromedriver.exe /F')#先清除残留的chromedriver进程
            #option = webdriver.ChromeOptions()
            #option.add_argument("--start-maximized")
            #driver = webdriver.Chrome(options=option)
            driver = webdriver.Chrome()
        elif browser == 'ie' or browser == 'internet explorer': # IE
            driver = webdriver.Ie()
        elif browser == "opera":
            driver = webdriver.Opera()
        elif browser == "phantomjs":
            driver = webdriver.PhantomJS()
        elif browser == 'edge':
            driver = webdriver.Edge()

        try:
            driver.maximize_window()
            self.driver = driver
        except Exception:
            # 手动抛出异常
            raise NameError("Not found %s browser,You can enter 'ie', 'ff', 'opera', 'phantomjs', 'edge' or 'chrome'." % browser)
            
    def __del__(self):
        try:
            #if not self.is_closed:
            self.quit()
        except AttributeError as e:
            print(e)
            pass

    '''
        设置元素等待
        presence_of_element_located 方法： 判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement
        visibility_of_element_located 方法： 判断某个元素是否被添加到了dom里并且可见，可见代表元素可显示且宽和高都大于0
    '''
    def elementWait(self, css, secs=10):
        # 判断表达式是否包含指定字符
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        # 提取元素定位方式和定位表达式
        by = css.split("=>")[0]
        value = css.split("=>")[1]
        try:
            if by == "id":
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.ID,value)))
            elif by == 'name':
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.NAME,value)))
            elif by == "class":
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, value)))
            elif by == "link_text":
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, value)))
            elif by == "partial_link":
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, value)))
            elif by == "tag":
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.TAG_NAME, value)))
            elif by == "xpath":
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.XPATH, value)))
            elif by == "css":
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, value)))
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','partial_link','tag','xpath','css'.")
        except Exception:
            raise NameError("%s The element is not found on the page: %s"%(self, css))
            #print ("%s The element is not found on the page: %s"%(self, css))

    '''
        获取指定元素对象
            表达式：  by=>value （by为定位方式,value为定位方式的表达式,例如:按照id定位某个元素,id=>"#"）
    '''
    def getElement(self, css):
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")
        self.elementWait(css,5)

        by = css.split("=>")[0]
        value = css.split("=>")[1]

        if by == 'id':
            element = self.driver.find_element_by_id(value)
        elif by == 'name':
            element = self.driver.find_element_by_name(value)
        elif by == 'class':
            element = self.driver.find_element_by_class_name(value)
        elif by == 'link_text':
            element = self.driver.find_element_by_link_text(value)
        elif by == 'partial_link':
            element = self.driver.find_element_by_partial_link_text(value)
        elif by == 'tag':
            element = self.driver.find_element_by_tag_name(value)
        elif by == 'xpath':
            element = self.driver.find_element_by_xpath(value)
        elif by == 'css':
            element = self.driver.find_element_by_css_selector(value)
        else:
            raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','partial_link','tag','xpath','css'.")
        return element
    
    '''
    定位元素列表，同 getElement 方法
    返回一组元素列表
    取其中的一个用for循环遍历
    for i in range(len(ele_list)):
        print (ele_list[i])
    '''    
    def getElements(self, css):
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        by = css.split("=>")[0]
        value = css.split("=>")[1]

        if by == 'id':
            elements = self.driver.find_elements_by_id(value)
        elif by == 'name':
            elements = self.driver.find_elements_by_name(value)
        elif by == 'class':
            elements = self.driver.find_elements_by_class_name(value)
        elif by == 'link_text':
            elements = self.driver.find_elements_by_link_text(value)
        elif by == 'partial_link':
            elements = self.driver.find_elements_by_partial_link_text(value)
        elif by == 'tag':
            elements = self.driver.find_elements_by_tag_name(value)
        elif by == 'xpath':
            elements = self.driver.find_elements_by_xpath(value)
        elif by == 'css':
            elements = self.driver.find_elements_by_css_selector(value)
        else:
            raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','partial_link','tag','xpath','css'.")
        return elements
        
    '''请求/打开指定链接'''
    def openUrl(self, url):
        self.driver.get(url)

    '''窗口最大化'''
    def maxWindows(self):
        self.driver.maximize_window()

    '''设置窗口指定宽高 '''
    def setWindowsSize(self, wide, high):
        self.driver.set_window_size(width=wide,height=high)

    '''添加文本到input,追加 '''
    def addText(self, css, massage):
        #self.elementWait(css)
        self.getElement(css).send_keys(massage)

    '''添加文本到input,清空新加'''
    def inputText(self, css, massage):
        #self.elementWait(css)
        element=self.getElement(css)
        element.clear()
        element.send_keys(massage)

    '''清空input中的文本 '''
    def clear(self, css):
        #self.elementWait(css)
        self.getElement(css).clear()

    '''上传附件，适合页面上是input标签的情况  '''
    def upload_input_att(self,css,att):
        element=self.getElement(css)
        element.send_keys(att)
        
    ''' 上传附件，调用autoit3脚本实现附件上传    '''
    def upload_att(self,css,att):
        autoit3_path=os.path.join(getcwd.get_cwd(),"api//upload.exe")
        self.getElement(css).click()
        os.system(autoit3_path+' '+att)

    '''鼠标左键单击'''
    def click(self, css):
        #self.elementWait(css)
        self.getElement(css).click()

    '''鼠标右键单击'''
    def rightClick(self, css):
        #self.elementWait(css)
        ActionChains(self.driver).context_click(self.getElement(css)).perform()

    '''
        滚动鼠标中键
         up_down : -1代表向下移动一个单位，1代表向上移动一个单位
    '''
    def mouseScroll(self,up_down):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,up_down)        
    
    '''移动鼠标到指定元素(默认在元素的中间位置)'''
    def moveToTargetElement(self, css):
        #self.elementWait(css)
        ActionChains(self.driver).move_to_element(self.getElement(css)).perform()

    '''移动鼠标到指定元素,并且指定位于元素的x,y偏移量(偏移量相对于元素的左上角)'''
    def moveToTargetElementWithOffset(self, css, xoffset, yoffset):
        #self.elementWait(css)
        ActionChains(self.driver).move_to_element_with_offset(self.getElement(css), xoffset, yoffset).perform()

    '''鼠标左键双击'''
    def doubleClick(self, css):
        #self.elementWait(css)
        ActionChains(self.driver).double_click(self.getElement(css)).perform()

    '''拖拽元素到指定元素处'''
    def dragAndDropToElement(self, sourceCss, targetCss):
        #self.elementWait(sourceCss)
        #self.elementWait(targetCss)
        ActionChains(self.driver).drag_and_drop(self.getElement(sourceCss),self.getElement(targetCss)).perform()

    '''拖拽元素指定偏移(该偏移是相对于当前鼠标的坐标偏移量)'''
    def dragAndDropToOffset(self, sourceCss, xoffset, yoffset):
        #self.elementWait(sourceCss)
        ActionChains(self.driver).drag_and_drop_by_offset(self.getElement(sourceCss), xoffset, yoffset).perform()

    '''鼠标左键点击链接文本 '''
    def clickLinkText(self, text):
        self.driver.find_element_by_partial_link_text(text).click()

    '''  关闭当前窗口'''
    def close(self):
        self.driver.close()

    '''关闭浏览器驱动'''
    def quit(self):
        self.driver.quit()

    '''提交指定表单'''
    def submit(self, css):
        #self.elementWait(css)
        self.getElement(css).submit()

    '''刷新当前页面,相当于点击F5'''
    def F5(self):
        self.driver.refresh()
    
    '''浏览器前进操作'''
    def forward(self):
        self.driver.forward()
    
    '''浏览器后退操作 '''
    def back(self):
        self.driver.back()

    '''执行指定的js代码'''
    def js(self, javaScript):
        self.driver.execute_script(javaScript)

    '''执行指定的脚本代码'''
    def runScript(self, script,ass):
        self.driver.execute_script(script,ass)

    '''获取指定元素的某个属性值'''
    def getAttribute(self, css, attr):
        #self.elementWait(css)
        self.getElement(css).get_attribute(attr)

    '''获取指定元素的文本内容,即value属性值'''
    def getText(self, css):
        #self.elementWait(css)
        return self.getElement(css).text

    '''判断元素是否可见'''
    def isDisplay(self, css):
        #self.elementWait(css)
        return self.getElement(css).is_displayed()

    '''判断元素是否启用'''
    def isEnabled(self, css):
        #self.elementWait(css)
        return self.getElement(css).is_enabled()

    '''判断元素是否选中,一般用于验证checkbox和radio'''
    def isSelected(self, css):
        #self.elementWait(css)
        return self.getElement(css).is_selected()

    '''获取当前页面的title'''
    def getTitle(self):
        return self.driver.title

    '''获取当前页面的url'''
    def getCurrentUrl(self):
        return self.driver.current_url

    '''截图,保存到指定路径下文件中'''
    def getScreenshot(self, fullFileName):
        #self.driver.get_screenshot_as_file(fullFileName)
        pngName=Screenshot(self.driver).savePngName(Sname=fullFileName)
        return pngName

    '''全局等待,Implicitly wait.All elements on the page. '''
    def wait(self, secs):
        self.driver.implicitly_wait(secs)
    
    '''强制等待多少秒'''
    def waitSleep(self,secs=2):
        time.sleep(secs)
    
    ''' 弹框警告-确认'''
    def alertAccept(self):
        # self.driver.switch_to_alert().accept() 废弃的方式
        self.driver.switch_to.alert.accept()

    '''弹框警告-取消 '''
    def alertDismiss(self):
        # self.driver.switch_to_alert().dismiss() 废弃的方式
        self.driver.switch_to.alert.dismiss()

    '''切换到指定的iframe'''
    def switchFrame(self, css):
        #self.elementWait(css)
        self.driver.switch_to.frame(self.getElement(css))

    '''切换到上一级(iframe)'''
    def switchFrameOut(self):
        self.driver.switch_to.default_content()

    '''
        打开新页面,并切换当前句柄为新页面的句柄
        (每个页面对应一个句柄handle,可以通过self.driver.window_handles查看所有句柄)
        --当前方法可能存在问题
    '''
    def openNewWindow(self):
        original_windows = self.driver.current_window_handle
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != original_windows:
                self.driver.switch_to.window(handle)

    '''
        等待查找元素是否被加载,默认5秒,每1秒检查一次
            --如果超时则对当前页面截图,并返回false
        可以用于判断元素是否存在，如果存在返回flag=true，否则返回false
    '''
    def findElement(self, css, sec=5,pictureName=None):
        try:
            self.elementWait(css, sec)
            return True
        except Exception:
            if pictureName != None:
                self.getScreenshot(pictureName)
            return False

    '''等待元素是否可见 '''
    def waitDisplayed(self,css,sec=5):
        element = self.getElement(css)
        i=1
        print("element.is_displayed: ",element.is_displayed())
        while element.is_displayed():
            if i > sec:
                break
            else:
                self.waitSleep(1)
                i=i+1

    '''
        通过value定位
        根据指定的值选中相应的下拉列表中的选项
            --如果没有指定的值则抛出异常
    '''
    def selectByValue(self, css, value):
        Select(self.getElement(css)).select_by_value(value)

    '''
        通过text定位
        根据指定的值选中相应的下拉列表中的选项
            --如果没有指定的值则抛出异常
    '''
    def selectByText(self, css, value):
        Select(self.getElement(css)).select_by_visible_text(value)

    '''
    获得页面验证码图片
    首先将有验证码的页面截图保存，然后通过页面元素定位方式定位到验证码，
    再通过图片管理库裁剪验证码所在区域，最后保存这个裁剪的验证码图片即是我们想要的图片
    '''
    def getVerifyImg(self,path,css):
        #self.elementWait(css)
        imgelement=self.getElement(css)#定位验证码
        imgelement.click()#这里每次调用这个函数时，都刷新下验证码
        time.sleep(2)
        
        img_path=path
        self.driver.get_screenshot_as_file(img_path+'page.png')
        img = Image.open(img_path+'page.png')
        
        #获取验证码位置坐标
        location = imgelement.location  #获取验证码x,y轴坐标
        size=imgelement.size  #获取验证码的长宽
        rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
        #print(rangle)
        
        # 用box裁剪出截图中验证码的所在区域
        reName='code.png'
        box = rangle  # 设置要裁剪的区域
        img_region = img.crop(box)  # 此时，region是一个新的图像对象
        img_region.save(img_path+reName)
        #img_region.show()
        return reName
    
    

    '''
    验证码只支持纯数字
    循环输入验证码，因为一遍可能不能正确识别，直到正确识别，再进行其他操作
    失败后重复读取，最多重复执行10次
    '''
    def readCode(self,css):
        accept = False
        code=''
        whileNum=0
        img_path=os.path.join(getcwd.get_cwd(),"img//")
        
        while not accept:
            try:
                whileNum=whileNum+1
                img_name=self.getVerifyImg(img_path,css)
                code=getVerifyCode().getCode(img_path,img_name)        
                #print('code：' + code)
        
                # 如果验证码没有识别正确，可能会弹出提示框，这里我们需要对提示框进行处理        
                # 在页面中寻找提示框
                time.sleep(1)
                res = EC.alert_is_present()(self.driver)
        
                # 如果弹出提示框
                if res:
                    # 点击提示框的确认，从新搜索一遍
                    res.accept()
                    time.sleep(1)
                else:
                    # 说明已经识别成功并搜索成功，跳出循环进行下一步操作
                    accept = True
                
                #如果第一次没有获取到验证码，则重复执行
                if len(code)!=4 and whileNum<10:
                    accept=False
                    #print('读取验证码失败，重复执行第 ',whileNum+1,' 次')
                if whileNum >= 10:
                    raise NameError('读取验证码失败，程序多次尝试任无法获得验证码')
                    
            except UnicodeDecodeError:
                accept = False
                time.sleep(1)            
        return code
    
    '''处理页面alert框,点击提示框的确认'''
    def checkAlert(self):
            # 在页面中寻找提示框
            time.sleep(2)
            res = EC.alert_is_present()(self.driver)  
           
            if res:  # 如果弹出提示框
                res.accept()    # 点击提示框的确认
                #res.dismiss()   #点击提示框的取消，或者叉掉提示框
                #print(res.text)    #打印提示框的文本信息
                #res.send_keys('提示信息！')    #输入文本
                return True
            return False
        
        
    """
    根据table的id(或其他定位)属性和table中的某一个元素定位其在table中的位置
    table包括表头，位置坐标都是从1开始算
    css：table的定位属性
    
    数据显示方式
    for i in range(len(table_list)):
        for j in range(len(table_list[i])):
            print(i,j,table_list[i][j])
   """
    def get_table_content(self,css): 
        # 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
        table_tr_list=self.driver.find_element(By.CLASS_NAME, css).find_elements(By.TAG_NAME, "tr")
        table_list = []  #存放table数据
        for tr in table_tr_list:    #遍历每一个tr
            #将每一个tr的数据根据td查询出来，返回结果为list对象
            table_td_list = tr.find_elements(By.TAG_NAME, "td")
            row_list = []
            for td in table_td_list:    #遍历每一个td
                row_list.append(td.text)    #取出表格的数据，并放入行列表里
            table_list.append(row_list)
        #print(table_list)
        return table_list


