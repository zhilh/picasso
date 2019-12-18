#-*- coding:utf-8 -*-
'''
Created on 2019年7月12日
@author: zhilh
Description: 常用的性能监控
'''
import subprocess
import os,re


#的到cpu利用率
def top_cpu(pkg_name):
    result = 0
    cmd = "adb shell dumpsys cpuinfo | grep -w " + pkg_name+":"
    temp = []
    # cmd = "adb shell top -n %s -s cpu | grep %s$" %(str(times), pkg_name)
    top_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    for info in top_info:
        temp.append(info.split()[2].decode()) # bytes转换为string
        break
    for i in temp:
        if i != "0%":
            print("cpu="+i)
            result = int(i.split("%")[0])
    return result

# 得到men的使用情况
def get_men(pkg_name):
    result = "0"
    cmd = "adb shell  dumpsys  meminfo %s"  %(pkg_name)
    temp = []
    m = []
    men_s = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    for info in men_s:
        temp.append(info.split())
    m.append(temp)
    for t in m:
        result = t[19][1]
        break
    return int(result.decode())

# 得到fps
def get_fps(pkg_name):
    _adb = "adb shell dumpsys gfxinfo %s | grep -A 128 'Execute'  | grep -v '[a-Z]' "%pkg_name
    result = os.popen(_adb).read().strip()
    result = result.split('\r\n')
    # r_result = [] # 总值
    # t_result = [] # draw,Process,Execute分别的值
    # f_sum = 0
    for i in result:
        l_result = i.split('\t')[-3:]
        f_sum = 0
        for j in l_result:
            r = re.search(r"\d+\.\d+", str(j))
            if r:
                f_sum += float(r.group())
            # t_result.append('%.2f'%f_sum)
        return float('%.2f'%f_sum)

def test(pkg_name):
    cpu=top_cpu(pkg_name)
    print(cpu)
    men=get_men(pkg_name)
    print(men)
    fps=get_fps(pkg_name)
    print(fps)

if __name__ == '__main__':
    test('com.vdin.ydjfn')


