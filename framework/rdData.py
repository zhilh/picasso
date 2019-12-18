#-*- coding:utf-8 -*-
'''
Created on 2018年11月15日
@author: zhilh
Description: 用于生成各种随机数
'''
import random
import time,datetime
from framework.data import ADDR,XING,MING



def getTimestamp():
    '''获取当前时间戳，10位'''
    return str(int(time.time()))

def getStrings(n=10,digit=True,upper=True,lower=True,spechars=True):
    ''' 随机产生N个字符，默认大写字母+小写字母+数字+特殊字符，digit：True首字母可以为数字，False首字母不能为数字'''
    #lists = [chr(i) for i in range(65,91)] + [chr(i) for i in range(97,123)] + [ str(i) for i in range(10)] #大写字母+小写字母+数字
    lists=[ str(i) for i in range(10)]  #数字
    if upper:
        lists=lists+[chr(i) for i in range(65,91)]  #加上大写字母
    if lower:
        lists=lists+[chr(i) for i in range(97,123)] #加上小写字母
    if spechars:
        lists=lists+['~','!','@','#','$','%','&','*','(',')','_','+']  #特殊字符
    #print(lists)

    num = random.sample(lists,n) 
    value = ''.join(num) #将取出的十个随机数进行重新合并
    while not digit:
        if not value[0].isdigit():#首位是否是数字
            break
        num = random.sample(lists,n) 
        value = ''.join(num) #将取出的十个随机数进行重新合并
    return value

def getUnicode(n=5):
    '''在unicode码中,汉字的范围是(0x4E00, 9FBF),收录了2万多个汉字,包括很多生僻的繁体字'''
    str=''
    for i in range(n):
        val=chr(random.randint(0x4e00, 0x9fbf))
        #str =f'{str}{val}'
        str=str+val
    return str

def getGBK2312(n=5):
    '''在gb2312码中,2对字符的编码采用两个字节相组合,第一个字节的范围是0xB0-0xF7, 第二个字节的范围是0xA1-0xFE, 收录了6千多常用汉字'''    
    str=''
    for i in range(n):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xf9)   # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
        val = f'{head:x}{body:x}'  # 相当于 '{0:x} {1:x}'.format(head, body)
        val = bytes.fromhex(val).decode('gb2312')
        #str =f'{str}{val}'
        str=str+val
    return str

def getInt(n=3):
    '''生成n位随机整数,首位不能为零'''
    digits=[0]
    while (digits[0])==0:
        digits = [random.randint(0,9) for i in range(n)] #随机生成n位0~9之间的随机数
    number = int(''.join(map(str, digits))) #转换为str>链接成一个字符串>转换为整数
    return number

def sampleInt(x=0,y=9):
    '''生成一个[x,y]之间的随机整数'''
    if x>y :
        z=y
        y=x 
        x=z 
    digits=list(range(x,y+1))          # 注意range的参数是包头不包尾。
    #digits.remove(5)                 # 从列表中去除某个数字
    #print(digits)
    number = random.sample(digits,1)[0]  # sample方法两个参数的意义是（列表，取几个值）
    return number

def getListItem(lists=[0],n=1):
    '''从一个list中随机返回n个元素'''
    if  not isinstance(lists,list):
        print("The variable %s is not of type list"%lists)
        return None
    map(str,lists)   #将列表内每个元素转换成字符格式
    if n>len(lists):
        n=sampleInt(1,len(lists))
    if n<1:
        n=1
    if len(lists) == 0:
        lists=[0]
    some = random.sample(lists , n)
    if len(some)<2:
        some=''.join(str(s) for s in some if s not in [None])
        #some = ''.join(some)
    return some
    
def getEmail( emailType=None, rang=None):
    '''生成随机邮件'''
    __emailtype = ["@qq.com", "@163.com", "@126.com", "@189.com"]
    # 如果没有指定邮箱类型，默认在 __emailtype中随机一个
    if emailType == None:
        __randomEmail = random.choice(__emailtype)
    else:
        __randomEmail = emailType
    # 如果没有指定邮箱长度，默认在4-10之间随机
    if rang == None:
        __rang = random.randint(4, 10)
    else:
        __rang = int(rang)
    __Number = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ"
    __randomNumber = "".join(random.choice(__Number) for i in range(__rang))
    _email = __randomNumber + __randomEmail
    return _email

def getDate(s=-100,e=0):
    '''随机取出日期段  (s<= t <=e) 内的一个日期，s = -100:当前时间减去100天；e = 0:当前时间'''
    now = time.time()
    start = time.localtime(now+s*86400) #将传入天数转换为秒，一天等于86400秒
    end = time.localtime(now+e*86400)
   
    start=time.mktime(start)    #生成开始时间戳
    end=time.mktime(end)    #生成结束时间戳
    if start > end: 
        tmp=start
        start=end
        end=tmp
    t=random.randint(start,end) #在开始和结束时间戳中随机取出一个
    
    date_touple=time.localtime(t)   #将时间戳生成时间元组
    date=time.strftime("%Y-%m-%d",date_touple)  #将时间元组转成格式化字符串（1976-05-21）
    return date

def getName():
    '''参数随机姓名'''
    x = random.randint(0,len(XING)) 
    m1 = random.randint(0,len(MING)) 
    m2 = random.randint(0,len(MING))    
    return(''+XING[x]+MING[m1]+MING[m2])


def getPhone():
    '''随机生成手机号码'''
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153",
       "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

def getIdNumber(sex=1):
    '''产生随机可用身份证号，sex = 1表示男性，sex = 0表示女性'''
    # 地址码产生
    addrInfo = random.randint(0, len(ADDR))  # 随机选择一个值
    addrId = ADDR[addrInfo][0]
    addrName = ADDR[addrInfo][1]
    idNumber = str(addrId)
    # 出生日期码
    start, end = "1960-01-01", "2000-12-30"  # 生日起止日期
    days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
    birthDays = datetime.datetime.strftime(
    datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d")
    idNumber = idNumber + str(birthDays)
    # 顺序码
    for i in range(2):  # 产生前面的随机值
        n = random.randint(0, 9)  # 最后一个值可以包括
        idNumber = idNumber + str(n)
        
    # 性别数字码
    sexId = random.randrange(sex, 10, step=2)  # 性别码
    idNumber = idNumber + str(sexId)
    # 校验码
    checkOut = getValidateCheckout(idNumber)
    idNumber = idNumber + str(checkOut)
    return idNumber, addrName, addrId, birthDays, sex, checkOut

def getValidateCheckout(id17):
    '''获得校验码算法'''
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 十七位数字本体码权重
    validate = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  # mod11,对应校验码字符值
    
    sum = 0
    mode = 0
    for i in range(0, len(id17)):
        sum = sum + int(id17[i]) * weight[i]
    
    mode = sum % 11
    return validate[mode]








