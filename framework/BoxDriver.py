#-*- coding:utf-8 -*-
'''
Created on 2019年7月26日
@author: zhilh
Description: 
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import win32gui
import win32con
import time
from enum import Enum

class BoxDriver(object):
    """
    selenium framework tool
    """

    """
    私有全局变量
    """
    _base_driver = None
    _by_char = None

    """
    构造方法
    """

    def __init__(self, browser_type=0, download_path="E:\\Downloads", by_char=",", profile=None):
        """
        构造方法：实例化 BoxDriver 时候使用
        :param browser_type: 浏览器类型
        :param by_char: 分隔符，默认使用","
        :param profile:
            可选择的参数，如果不传递，就是None
            如果传递一个 profile，就会按照预先的设定启动火狐
            去掉遮挡元素的提示框等
        """
        self._by_char = by_char
        if browser_type == 0 or browser_type == Browser.Chrome:
            profile = webdriver.ChromeOptions()
            # profile.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
            # download.default_directory：设置下载路径
            # profile.default_content_settings.popups：设置为 0 禁止弹出窗口
            prefs = {'profile.default_content_settings.popups': 0,
                     'download.default_directory': download_path}
            profile.add_experimental_option('prefs', prefs)
            driver = webdriver.Chrome(chrome_options=profile)
            # driver = webdriver.Chrome(executable_path='D:\\chromedriver.exe', chrome_options=options)


        elif browser_type == 1 or browser_type == Browser.Firefox:
            # if profile is not None:
                # profile = FirefoxProfile(profile)

            profile = webdriver.FirefoxProfile()
            # 指定下载路径
            profile.set_preference('browser.download.dir', download_path)
            # 设置成 2 表示使用自定义下载路径；设置成 0 表示下载到桌面；设置成 1 表示下载到默认路径
            profile.set_preference('browser.download.folderList', 2)
            # 在开始下载时是否显示下载管理器
            profile.set_preference('browser.download.manager.showWhenStarting', False)
            # 对所给出文件类型不再弹出框进行询问
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')

            driver = webdriver.Firefox(firefox_profile=profile)

        elif browser_type == Browser.Ie:
            driver = webdriver.Ie()
        else:
            driver = webdriver.PhantomJS()
        try:
            self._base_driver = driver
            self._by_char = by_char
        except Exception:
            raise NameError("Browser %s Not Found! " % browser_type)

    """
    私有方法
    """

    def _convert_selector_to_locator(self, selector):
        """
        转换自定义的 selector 为 Selenium 支持的 locator
        :param selector: 定位字符，字符串类型，"i, xxx"
        :return: locator
        """
        if self._by_char not in selector:
            return By.ID, selector

        selector_by = selector.split(self._by_char)[0].strip()
        selector_value = selector.split(self._by_char)[1].strip()
        if selector_by == "i" or selector_by == 'id':
            locator = (By.ID, selector_value)
        elif selector_by == "n" or selector_by == 'name':
            locator = (By.NAME, selector_value)
        elif selector_by == "c" or selector_by == 'class_name':
            locator = (By.CLASS_NAME, selector_value)
        elif selector_by == "l" or selector_by == 'link_text':
            locator = (By.LINK_TEXT, selector_value)
        elif selector_by == "p" or selector_by == 'partial_link_text':
            locator = (By.PARTIAL_LINK_TEXT, selector_value)
        elif selector_by == "t" or selector_by == 'tag_name':
            locator = (By.TAG_NAME, selector_value)
        elif selector_by == "x" or selector_by == 'xpath':
            locator = (By.XPATH, selector_value)
        elif selector_by == "s" or selector_by == 'css_selector':
            locator = (By.CSS_SELECTOR, selector_value)
        else:
            raise NameError("Please enter a valid selector of targeting elements.")

        return locator

    def _locate_element(self, selector):
        """
        to locate element by selector
        :arg
        selector should be passed by an example with "i,xxx"
        "x,//*[@id='langs']/button"
        :returns
        DOM element
        """
        locator = self._convert_selector_to_locator(selector)
        if locator is not None:
            element = self._base_driver.find_element(*locator)
        else:
            raise NameError("Please enter a valid locator of targeting elements.")

        return element

    def _locate_elements(self, selector):
        """
        to locate element by selector
        :arg
        selector should be passed by an example with "i,xxx"
        "x,//*[@id='langs']/button"
        :returns
        DOM element
        """
        locator = self._convert_selector_to_locator(selector)
        if locator is not None:
            elements = self._base_driver.find_elements(*locator)
        else:
            raise NameError("Please enter a valid locator of targeting elements.")

        return elements

    """
    cookie 相关方法
    """

    def clear_cookies(self):
        """
        clear all cookies after driver init
        """
        self._base_driver.delete_all_cookies()

    def add_cookies(self, cookies):
        """
        Add cookie by dict
        :param cookies:
        :return:
        """
        self._base_driver.add_cookie(cookie_dict=cookies)

    def add_cookie(self, cookie_dict):
        """
        Add single cookie by dict
        添加 单个 cookie
        如果该 cookie 已经存在，就先删除后，再添加
        :param cookie_dict: 字典类型，有两个key：name 和 value
        :return:
        """
        cookie_name = cookie_dict["name"]
        cookie_value = self._base_driver.get_cookie(cookie_name)
        if cookie_value is not None:
            self._base_driver.delete_cookie(cookie_name)

        self._base_driver.add_cookie(cookie_dict)

    def remove_cookie(self, name):
        """
        移除指定 name 的cookie
        :param name: 
        :return: 
        """
        # 检查 cookie 是否存在，存在就移除
        old_cookie_value = self._base_driver.get_cookie(name)
        if old_cookie_value is not None:
            self._base_driver.delete_cookie(name)

    """
    浏览器本身相关方法
    """

    def refresh(self, url=None):
        """
        刷新页面
        如果 url 是空值，就刷新当前页面，否则就刷新指定页面
        :param url: 默认值是空的
        :return:
        """
        if url is None:
            self._base_driver.refresh()
        else:
            self._base_driver.get(url)

    def maximize_window(self):
        """
        最大化当前浏览器的窗口
        :return:
        """
        self._base_driver.maximize_window()

    def navigate(self, url):
        """
        打开 URL
        :param url:
        :return:
        """
        self._base_driver.get(url)

    def quit(self):
        """
        退出驱动
        :return:
        """
        self._base_driver.quit()

    def close_browser(self):
        """
        关闭浏览器
        :return:
        """
        self._base_driver.close()

    """
    基本元素相关方法
    """

    def type(self, selector, text):
        """
        Operation input box.

        Usage:
        driver.type("i,el","selenium")
        """
        el = self._locate_element(selector)
        el.clear()
        el.send_keys(text)

    def click(self, selector):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.click("i,el")
        """
        el = self._locate_element(selector)
        el.click()

    def click_eles(self,selector):
        '''
        循环点击一组元素中的每个元素
        :param selector:
        :return:
        '''
        counts = self.count_elements(selector)
        for i in range(counts):
            eles = self._locate_elements(selector)
            eles[i].click()

    def click_eles_i(self,selector,i):
        '''
        点击一组元素中的第几个元素
        :param selector:
        :param i: 第几个元素
        :return:
        '''
        eles = self._locate_elements(selector)
        eles[i].click()

    def click_by_enter(self, selector):
        """
        It can type any text / image can be located  with ENTER key

        Usage:
        driver.click_by_enter("i,el")
        """
        el = self._locate_element(selector)
        el.send_keys(Keys.ENTER)

    def click_by_text(self, text):
        """
        Click the element by the link text

        Usage:
        driver.click_text("新闻")
        """
        self._locate_element('p%s' % self._by_char + text).click()

    def submit(self, selector):
        """
        Submit the specified form.

        Usage:
        driver.submit("i,el")
        """
        el = self._locate_element(selector)
        el.submit()

    def move_to(self, selector):
        """
        to move mouse pointer to selector
        :param selector:
        :return:
        """
        el = self._locate_element(selector)
        ActionChains(self._base_driver).move_to_element(el).perform()

    def right_click(self, selector):
        """
        鼠标右击
        :param selector:
        :return:
        """
        el = self._locate_element(selector)
        ActionChains(self._base_driver).context_click(el).perform()

    def double_click(self,selector):
        '''
        鼠标双击
        :param selector: （想要双击的元素）元素定位
        :return: 无
        '''
        ele = self._locate_element(selector)
        ActionChains(self._base_driver).double_click(ele).perform()

    def count_elements(self, selector):
        """
        数一下元素的个数
        :param selector: 定位符
        :return:
        """
        els = self._locate_elements(selector)
        return len(els)

    def drag_element(self, source, target):
        """
        拖拽元素
        :param source:
        :param target:
        :return:
        """

        el_source = self._locate_element(source)
        el_target = self._locate_element(target)

        if self._base_driver.w3c:
            ActionChains(self._base_driver).drag_and_drop(el_source, el_target).perform()
        else:
            ActionChains(self._base_driver).click_and_hold(el_source).perform()
            ActionChains(self._base_driver).move_to_element(el_target).perform()
            ActionChains(self._base_driver).release(el_target).perform()

    def lost_focus(self):
        """
        当前元素丢失焦点
        :return:
        """
        ActionChains(self._base_driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()

    """
    <select> 元素相关
    """

    def select_by_index(self, selector, index):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.select_by_index("i,el")
        """
        el = self._locate_element(selector)
        Select(el).select_by_index(index)

    def get_selected_text(self, selector):
        """
        获取 Select 元素的选择的内容
        :param selector: 选择字符 "i, xxx"
        :return: 字符串
        """
        el = self._locate_element(selector)
        selected_opt = Select(el).first_selected_option()
        return selected_opt.text

    def select_by_visible_text(self, selector, text):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.select_by_index("i,el")
        """
        el = self._locate_element(selector)
        Select(el).select_by_visible_text(text)

    def select_by_value(self, selector, value):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.select_by_index("i,el")
        """
        el = self._locate_element(selector)
        Select(el).select_by_value(value)

    """
    JavaScript 相关
    """

    def execute_js(self, script):
        """
        Execute JavaScript scripts.

        Usage:
        driver.js("window.scrollTo(200,1000);")
        """
        self._base_driver.execute_script(script)

    """
    元素属性相关方法
    """

    def get_value(self, selector):
        """
        返回元素的 value
        :param selector: 定位字符串
        :return:
        """
        el = self._locate_element(selector)
        return el.get_attribute("value")

    def get_attribute(self, selector, attribute):
        """
        Gets the value of an element attribute.

        Usage:
        driver.get_attribute("i,el","type")
        """
        el = self._locate_element(selector)
        return el.get_attribute(attribute)

    def get_text(self, selector):
        """
        Get element text information.

        Usage:
        driver.get_text("i,el")
        """
        el = self._locate_element(selector)
        return el.text

    def get_displayed(self, selector):
        """
        Gets the element to display,The return result is true or false.

        Usage:
        driver.get_display("i,el")
        """
        el = self._locate_element(selector)
        return el.is_displayed()

    def get_exist(self, selector):
        '''
        该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
        :param self:
        :param selector: 元素定位，如'id,account'
        :return: 布尔值
        '''
        flag = True
        try:
            self._locate_element(selector)
            return flag
        except:
            flag = False
            return flag

    def get_enabled(self,selector):
        '''
        判断页面元素是否可点击
        :param selector: 元素定位
        :return: 布尔值
        '''
        if self._locate_element(selector).is_enabled():
            return True
        else:
            return False

    def get_title(self):
        '''
        Get window title.

        Usage:
        driver.get_title()
        '''
        return self._base_driver.title

    def get_url(self):
        """
        Get the URL address of the current page.

        Usage:
        driver.get_url()
        """
        return self._base_driver.current_url

    def get_selected(self, selector):
        """
        to return the selected status of an WebElement
        :param selector: selector to locate
        :return: True False
        """
        el = self._locate_element(selector)
        return el.is_selected()

    def get_text_list(self, selector):
        """
        根据selector 获取多个元素，取得元素的text 列表
        :param selector:
        :return: list
        """

        el_list = self._locate_elements(selector)

        results = []
        for el in el_list:
            results.append(el.text)

        return results

    """
    弹出窗口相关方法
    * 如果弹框的元素可以F12元素查看，则直接使用点击，获取元素等方法
    * 如果弹框元素无法查看，则使用如下方法可以搞定
    """
    def accept_alert(self):
        '''
            Accept warning box.

            Usage:
            driver.accept_alert()
            '''
        self._base_driver.switch_to.alert.accept()

    def dismiss_alert(self):
        '''
        Dismisses the alert available.

        Usage:
        driver.dismissAlert()
        '''
        self._base_driver.switch_to.alert.dismiss()

    def get_alert_text(self):
        '''
        获取 alert 弹出框的文本信息
        :return: String
        '''
        return self._base_driver.switch_to.alert.text

    def type_in_alert(self,text):
        '''在prompt对话框内输入内容'''
        self._base_driver.switch_to.alert.send_keys(text)
        self.forced_wait(1)

    def alert_new_display_none(self,selector_by_id_value):
        '''
        使用 JS 处理新型弹出框
        :param selector_by_id_value: id方式定位弹出框(div)的 value 值
        :return: 无
        '''
        js = 'document.getElementById("%s").style.display="none";' %selector_by_id_value
        self._base_driver.execute_script(js)


    '''
    进入框架、退出框架
    '''
    def switch_to_frame(self, selector):
        """
        Switch to the specified frame.

        Usage:
        driver.switch_to_frame("i,el")
        """
        el = self._locate_element(selector)
        self._base_driver.switch_to.frame(el)

    def switch_to_default(self):
        """
        Returns the current form machine form at the next higher level.
        Corresponding relationship with switch_to_frame () method.

        Usage:
        driver.switch_to_frame_out()
        """
        self._base_driver.switch_to.default_content()

    '''
    切换不同页面窗口
    '''
    def switch_to_window_by_title(self, title):
        for handle in self._base_driver.window_handles:
            self._base_driver.switch_to.window(handle)
            if self._base_driver.title == title:
                break

            self._base_driver.switch_to.default_content()

    def open_new_window(self, selector):
        '''
        Open the new window and switch the handle to the newly opened window.

        Usage:
        driver.open_new_window()
        '''
        original_windows = self._base_driver.current_window_handle
        el = self._locate_element(selector)
        el.click()
        all_handles = self._base_driver.window_handles
        for handle in all_handles:
            if handle != original_windows:
                self._base_driver._switch_to.window(handle)

    def save_window_snapshot(self, file_name):
        """
        save screen snapshot
        :param file_name: the image file name and path
        :return:
        """
        driver = self._base_driver
        driver.save_screenshot(file_name)

    def save_window_snapshot_by_io(self):
        """
        保存截图为文件流
        :return:
        """
        return self._base_driver.get_screenshot_as_base64()

    def save_element_snapshot_by_io(self, selector):
        """
        控件截图
        :param selector:
        :return:
        """
        el = self._locate_element(selector)
        return el.screenshot_as_base64

    """
    等待方法
    """

    def forced_wait(self, seconds):
        """
        强制等待
        :param seconds:
        :return:
        """
        time.sleep(seconds)

    def implicitly_wait(self, seconds):
        """
        Implicitly wait. All elements on the page.
        :param seconds 等待时间 秒
        隐式等待

        Usage:
        driver.implicitly_wait(10)
        """
        self._base_driver.implicitly_wait(seconds)

    def explicitly_wait(self, selector, seconds):
        """
        显式等待
        :param selector: 定位字符
        :param seconds: 最长等待时间，秒
        :return:
        """
        locator = self._convert_selector_to_locator(selector)

        WebDriverWait(self._base_driver, seconds).until(EC.presence_of_element_located(locator))

    """上传"""
    def upload_input(self,selector,file):
        '''
        上传文件 （ 标签为 input 类型，此类型最常见，最简单）
        :param selector: 上传按钮定位
        :param file: 将要上传的文件（绝对路径）
        :return: 无
        '''
        self._locate_element(selector).send_keys(file)

    def upload_not_input(self,file,browser_type='Chrome'):
        '''
        上传文件 （ 标签不是 input 类型，使用 win32gui,得先安装 pywin32 依赖包）
                                                pip install pywin32
        :param browser_type: 浏览器类型（Chrome浏览器和Firefox浏览器的有区别）
        :param file: 将要上传的文件（绝对路径）
        单个文件：file1 = 'C:\\Users\\list_tuple_dict_test.py'
        同时上传多个文件：file2 = '"C:\\Users\\list_tuple_dict_test.py" "C:\\Users\\class_def.py"'
        :return: 无
        '''
        # Chrome 浏览器是'打开'
        # 对话框
        # 下载个 Spy++ 工具，定位“打开”窗口，定位到窗口的类(L):#32770, '打开'为窗口标题
        if browser_type == 'Chrome':
            dialog = win32gui.FindWindow('#32770', u'打开')
        elif browser_type == 'Firefox':
            # Firefox 浏览器是'文件上传'
            # 对话框
            dialog = win32gui.FindWindow('#32770', u'文件上传')
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
        ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
        # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
        Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)
        # 确定按钮Button
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)
        # 往输入框输入绝对地址
        win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, file)
        # 按button
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)
        # 获取属性
        # print(upload.get_attribute('value'))

    """下载 //TODO"""
    def download(self,download_path,file_type,download_selector):
        '''
        下载（设置指定下载路径，不用每次都弹出对话框选择保存路径）
        :param download_path: 设置默认下载路径
        :param file_type: 默认下载文件类型
        :param download_selector: 下载元素定位
        :return:
        '''
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.dir', download_path)
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')

        driver = webdriver.Firefox(firefox_profile=profile)



    """
    表单数据提交:
        页面校验
        数据库校验
        某条记录选择，编辑，删除
    """
    def del_edit_choose_the_row(self, selector_of_next_page, selector_of_trs_td, selector_of_del_edit_choose,expected_td_value):
        """
        页面表单，选中/编辑/删除 指定内容的行（带多页翻页功能）
        :param selector_of_next_page: ‘下一页’定位，如：'l,下页'
        :param selector_of_trs_td: 所有行的某一列的定位，如 ranzhi 成员列表中，获取所有行的“真实姓名”那列：'x,/html/body/div/div/div/div[2]/div/div/table/tbody//tr/td[2]'
        :param selector_of_del_edit_choose: 指定要操作(删除/编辑/选择)的列，如 ranzhi 成员列表中,获取期望删除的列：'x,/html/body/div/div/div/div[2]/div/div/table/tbody/tr[%d]/td[11]/a[3]'
        :param expected_td_value: 期望的列内容，如ranzhi 成员列表中期望的“真实姓名”: '华仔'
        :return:无
        """

        td_values = self.get_text_list(selector_of_trs_td)
        for i in range(len(td_values)):
            if td_values[i] == expected_td_value:
                print('%s在第%d行显示(首页)！' % (td_values[i], i + 1))
                self.forced_wait(2)
                self.click(selector_of_del_edit_choose % (i + 1))
                break
        try:
            while (self.get_enabled(selector_of_next_page)):
                self.click(selector_of_next_page)
                self.forced_wait(2)
                td_values = self.get_text_list(selector_of_trs_td)
                for i in range(len(td_values)):
                    if td_values[i] == expected_td_value:
                        print('%s在第%d行显示(非首页)' % (td_values[i], i + 1))
                        self.forced_wait(3)
                        self.click(selector_of_del_edit_choose % (i + 1))
                continue
        except Exception as e:
            print('%s 操作成功！' % expected_td_value)

    def assert_new_record_exist_in_table(self, selector_of_next_page, selector_of_trs_td, expected_td_value):
        '''
        此方法针对页面列表（带多页翻页功能），都可以判断新增记录是否添加成功！
        若新增成功，则返回 True 布尔值；否则返回 False 布尔值
        :param selector_of_next_page: "下一页"定位，如：'l,下页'
        :param selector_of_trs_td:所有行的某一列的定位，如： 'x,/html/body/div/div[2]/div/div[1]/div/table/tbody//tr/td[2]'
        :param expected_td_value:期望的列内容,如：'华仔'
        :return: 布尔值
        '''
        # first_count_per_page = self.count_elements(selector_of_real_record)
        # print('当前设置为每页显示 %s 条记录' % first_count_per_page)
        real_records = self.get_text_list(selector_of_trs_td)
        for real_record in real_records:
            if real_record == expected_td_value:
                return True
        # count_per_page_whiles = 0
        try:

            while (self.get_enabled(selector_of_next_page)):
                self.click(selector_of_next_page)
                self.forced_wait(2)
                # count_per_page_while = driver.count_elements("x,//tbody//tr/td[2]")
                # count_per_page_whiles += count_per_page_while
                next_page_real_records = self.get_text_list(selector_of_trs_td)
                for next_page_real_record in next_page_real_records:
                    if next_page_real_record == expected_td_value:
                        # self.log.info('记录新增成功！新增记录 %s 不是在第一页被找到！'%expect_new_record)
                        return True
                continue
        except Exception as e:
            # count_page_real_show = count_per_page_whiles + first_count_per_page
            # print("页面实际显示记录条数：%s" % count_page_real_show)
            # 页面统计总数 VS 页面实际显示记录总数
            # assert count_page_real_show == int(total_num)
            # print("‘页面实际显示记录总数’ 与 ‘页面统计显示记录总数’ 相同！")

            # raise NameError("页面表单中无此数据，原因：(1)请查询待验证的数据是否输入正确？(2)或者'下页'翻页定位是否正确？")
            print("页面表单中无此数据，原因：(1)请查询待验证的数据是否输入正确？(2)或者'下页'翻页定位是否正确？")
            return False

#@unique
class Browser(Enum):
    """
    定义支持的浏览器，支持Chrome，Firefox，Ie
    """
    Chrome = 0
    Firefox = 1
    Ie = 2
    

    