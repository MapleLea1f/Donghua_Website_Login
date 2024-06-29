from get import getinfo
import requests


#edge浏览器登录cookie
getinfo().login_in()
#能进入堡垒机页面，但是登录失效，猜测是get的时候自动获取了时间戳,需要模拟get请求

cookies = getinfo().cookies
# print(cookies)
headers = getinfo().headers
# print(headers)


url='https://webproxy.dhu.edu.cn/https/446a5061214023323032323131446855152f7f4845a0b976a6a0aa1d0121c0/dhu/selectcourse/toSH'
data = {
    'isSelectCourse':'true'
}

response = requests.get(url,cookies=cookies,headers=headers)
print(response.text)
data1 = {
    'courseCode': '010142',
}

response = requests.post('https://webproxy.dhu.edu.cn/https/446a5061214023323032323131446855152f7f4845a0b976a6a0aa1d0121c0/dhu/selectcourse/accessJudge?vpn-12-o2-jwgl.dhu.edu.cn', cookies=cookies, headers=headers, data=data1)
print(response.text)