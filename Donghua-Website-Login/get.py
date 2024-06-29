#coding:utf-8
import getPass
import requests
import time 
import re
from datetime import datetime


#登入流程：
# 1. 访问登录页面，获取cookies
#cookie不变，但是对应cookie需要一个post提交对应数据来维持登陆状态
# 2. 模拟登录请求，对登录页面进行post请求，提交用户名密码等信息

class getinfo:
    # 登录页面的url
    def __init__(self):
        self.url = 'https://webproxy.dhu.edu.cn/https/446a50612140233230323231314468551c396b0a0faca42deda1bb464c2c/authserver/login?service=https%3A%2F%2Fwebproxy.dhu.edu.cn%3A443%2Flogin%3Fcas_login%3Dtrue'
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'route=8768cab8c7e7ee1c6799ad807f94da0a; show_vpn=0; show_fast=0; heartbeat=1; show_faq=0; wengine_vpn_ticketwebproxy_dhu_edu_cn=22c3a065576f3be2; refresh=1',
            'Origin': 'https://webproxy.dhu.edu.cn',
            'Referer': 'https://webproxy.dhu.edu.cn/https/446a5061214023323032323131446855152f7f4845a0b976a6a0aa1d0121c0/dhu/selectcourse/toSH',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        self.page_info=requests.get(self.url, headers=self.headers)
        self.cookies=self.page_info.cookies.get_dict()
        sno=input('请输入学号：')
        passw=input('请输入密码：')

        lt=re.findall(r'name="lt" value="([^"]+)"', self.page_info.text)[0]
        dllt=re.findall(r'name="dllt" value="([^"]+)"', self.page_info.text)[0]
        execution=re.findall(r'name="execution" value="([^"]+)"', self.page_info.text)[0]
        eventId=re.findall(r'name="_eventId" value="([^"]+)"', self.page_info.text)[0]
        rmShown=re.findall(r'name="rmShown" value="([^"]+)"', self.page_info.text)[0]
        salt=re.findall(r'id="pwdDefaultEncryptSalt" value="([^"]+)"', self.page_info.text)[0]
        pwd=getPass.getCryptPass(passw=passw,salt=salt)
        
        
        
        self.data = {
            'username': sno,
            'password': pwd,
            'lt': lt,
            'dllt': dllt,
            'execution': execution,
            '_eventId': eventId,
            'rmShown': rmShown,
        }
    def login_in(self):
        session=requests.session()
        response=session.post(self.url, headers=self.headers, cookies=self.page_info.cookies, data=self.data)
        
        date=response.headers.get('Date')
        print(date)
        server_time = time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
    
    # 使用mktime函数将结构化时间转换为时间戳
        timestamp = time.mktime(server_time)

        print(f"Server time: {date} -> Timestamp: {timestamp}")
        # 生成一个包含从000到999的字符串列表
        number_strings = [f"{i:03d}" for i in range(1000)]

        # 打印列表
        for number in number_strings:
            session.get('https://webproxy.dhu.edu.cn/config?_t={0}{1}'.format(str(int(timestamp)),str(number)))
        if getinfo().check_response(response):
            print('登陆成功')
            print(response.url)
        else:    
            print('登陆失败')

        
    @staticmethod
    def check_response(response):
        if '堡垒机' in response.text:
            return True
            
        else:
            return False

