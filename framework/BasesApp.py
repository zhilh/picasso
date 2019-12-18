#-*- coding:utf-8 -*-
'''
Created on 2019年2月22日
@author: zhilh
Description: app端自动化基础操作封装
'''
import time
from appium import webdriver as apmdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from selenium.common.exceptions import NoSuchElementException,TimeoutException

from framework.Screenshot import Screenshot
from framework.readConfig import ReadConfig

cf=ReadConfig()
APP_PARA = {'appPackage': cf.get_config('APPNAME_YDJFN', 'appPackage'),
            'appActivity': cf.get_config('APPNAME_YDJFN', 'appActivity'),
            }
login_user = cf.get_config('APPNAME_YDJFN', 'login_user')
login_pass = cf.get_config('APPNAME_YDJFN', 'login_pass')

class AppDriver(object):
    def __init__(self,kwargs=APP_PARA):
        '''初始化链接参数'''
        self.desired_caps = {}
        self.desired_caps['automationName'] = 'appium' #定义测试引擎，使用的android-sdk版本小于17时，使用Selendroid，大于等于17时使用Appium，默认是Appium
        self.desired_caps['platformName'] = 'Android' #测试平台，通常用于移动设备，值有：Android、IOS、FirefoxOS
        self.desired_caps['platformVersion'] = '5.1.1' #测试平台版本，根据设备的固件版本指定，例如Android的4.2、IOS的7.1
        self.desired_caps['deviceName'] = '' #IOS设备型号，android设备无效
        self.desired_caps['udid'] = '' #连接设备的Uid，主要针对IOS
        self.desired_caps['newCommandTimeout'] = 300 #为了结束Appium会话，会设置一个等待从客户端发送命令的超时时间，默认为60秒，一般不需要设置
        #self.desired_caps['app'] = '' #要安装的app的文件路径，可以是本地的绝对路径，也可以是远程网络路径　
        self.desired_caps['unicodeKeyboard'] = True #输入中文设置，使用unicodeKeyboard的编码方式来发送字符串
        self.desired_caps['resetKeyboard'] = True   #输入中文设置，将键盘给隐藏起来
        #self.desired_caps["noSign"]=True #安装时不对apk进行重签名，设置很有必要，否则有的apk在重签名之后无法正常使用
        #self.desired_caps["noReset"]=True #不需要每次都安装apk
        self.desired_caps['appPackage'] = kwargs.get("appPackage")   #设置app的主包名，告诉Appium需要启动的app
        self.desired_caps['appActivity'] = kwargs.get("appActivity")   #设置app的主类名，启动的activity
        self.login_user=login_user
        self.login_pass=login_pass

        try:
            self.driver = apmdriver.Remote('http://127.0.0.1:4723/wd/hub', self.desired_caps)
            #return self.driver
        except Exception as e:
            raise NameError ("Original error:",e)

    '''    
    @staticmethod
    def get_driver(self):
        if self.driver is None:
            self.driver.mutex.acquire()
            if self.driver is None:
                self.driver = apmdriver.Remote('http://127.0.0.1:4723/wd/hub', self.desired_caps)
            else:
                return self.driver
            self.mutex.release()
        else:
            print ("you have been created a session")
        return self.driver'''
    
    def __del__(self):
        pass
        #self.driver.quit()
    
    def quit(self):
        #self.driver.reset() #重置app，删除缓存数据
        self.driver.quit() #退出app

    def elementWait(self, css, secs=5):
        '''设置元素等待'''
        # 判断表达式是否包含指定字符
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        # 提取元素定位方式和定位表达式
        by = css.split("=>")[0]
        value = css.split("=>")[1]
        try:
            if by == "resource_id":
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.ID,value)))
            elif by == 'text':
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.NAME,value)))
            elif by == "class":
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, value)))
            elif by == "content_desc":
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, value)))#By.content_desc???
            elif by == "xpath":
                WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.XPATH, value)))
            else:
                raise NameError("Please enter the correct targeting elements,'resource_id','text','class','content_desc','xpath'.")
        except Exception:
            raise NameError("%s The element is not found on the page: %s"%(self, css))
        #except NoSuchElementException:
        #    print('Not found')
        #except TimeoutException:
        #    print('Time out')
            
    def getElement(self, css):
        '''
            获取指定元素对象
                表达式：  by=>value （by为定位方式,value为定位方式的表达式,例如:按照id定位某个元素,id=>"#"）
        '''
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")
        self.elementWait(css,10)
        by = css.split("=>")[0]
        value = css.split("=>")[1]

        if by == 'resource_id':
            #根据资源resource-id获取对象
            #这里的id和 UIAutomatorView 中该元素的 resource id是一致的。
            #Android 4.3 以上系统才会有 resource id
            element = self.driver.find_element_by_id(value)
        elif by == 'text':
            #通过元素 text 来查找元素
            #这里的name跟 UIAutomatorView 中该元素的 Text是一致的。
            #不建议使用这种定位方法，因为 Appium v1.0 已经不建议使用通过name进行定位的方式。
            element = self.driver.find_element_by_name(value)
        elif by == 'class':
            #通过元素class name来查找元素
            #这里的class name跟 UIAutomatorView 中该元素的 class 是一致的。
            #多数情况下 class name不是唯一的
            element = self.driver.find_element_by_class_name(value)
        elif by == 'content_desc':
            #通过元素content-desc来查找元素
            #这里的accessibility id 跟 UIAutomatorView 中该元素的 content-desc 是一致的
            element = self.driver.find_element_by_accessibility_id(value)
        elif by == 'xpath':
            #通过元素xpath来查找元素
            #扩展版本的LazyUiAutomatorViewer可以看到最下方有xpath属性,也可以直接通过层次关系写出元素的xpath
            element = self.driver.find_element_by_xpath(value)
        else:
            raise NameError("Please enter the correct targeting elements,'resource_id','text','class','content_desc','xpath'.")
        return element

    def inputText(self, css, massage):
        '''添加文本到input,清空新加'''
        #self.elementWait(css)
        element=self.getElement(css)
        element.clear()
        element.send_keys(massage)

    def click(self, css):
        '''元素点击'''
        #self.elementWait(css)
        self.getElement(css).click()
    
    def getText(self, css):
        '''返回元素的文本值'''
        #self.elementWait(css)
        return self.getElement(css).text
    
    def waitSleep(self,secs=2):
        '''强制等待多少秒'''
        time.sleep(secs)

    def findElement(self, css, sec=5,pictureName=None):
        '''等待查找元素是否被加载,默认5秒,每1秒检查一次
             --如果超时并且传入了文件名，则对当前页面截图,并返回false
            可以用于判断元素是否存在，如果存在返回flag=true，否则返回false '''
        try:
            self.elementWait(css, sec)
            return True
        except Exception:
            if pictureName != None:
                self.getScreenshot(pictureName)
            return False
    
    #向上滑动屏幕
    def swipeUp(self, t=500, n=1):
        '''向上滑动屏幕'''
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.5     # x坐标
        y1 = l['height'] * 0.75   # 起始y坐标
        y2 = l['height'] * 0.25   # 终点y坐标
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)
    
    #向下滑动屏幕    
    def swipeDown(self, t=500, n=1):
        '''向下滑动屏幕'''
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.5          # x坐标
        y1 = l['height'] * 0.25        # 起始y坐标
        y2 = l['height'] * 0.75         # 终点y坐标
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2,t)
    
    #向左滑动屏幕
    def swipLeft(self, t=500, n=1):
        '''向左滑动屏幕'''
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.75
        y1 = l['height'] * 0.5
        x2 = l['width'] * 0.05
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)
    
    #向右滑动屏幕
    def swipRight(self, t=500, n=1):
        '''向右滑动屏幕'''
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.05
        y1 = l['height'] * 0.5
        x2 = l['width'] * 0.75
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)

    def getScreenshot(self, fullFileName):
        '''截图,保存到指定路径下文件中'''
        pngName=Screenshot(self.driver).savePngName(Sname=fullFileName)
        return pngName
      
    