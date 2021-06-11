from collections import defaultdict

import requests

local_url = 'http://localhost:8000/'
remote_url = 'http://45.134.171.215:8000/'
internal_url = 'http://192.168.1.111:8000/'



def login_logout_test(url, data):
    print('login_logout_test:')
    resp = requests.post(url + 'login/log_in', json=data)
    cookie = resp.cookies
    print(cookie.items())
    print(resp.json())
    resp = requests.post(url + 'login/log_in', json=data, cookies=cookie)
    print(resp.json())
    resp = requests.post(url + 'login/log_out', cookies=cookie)
    print(resp.json())

register_data0 = {
    "usr": "jinchenzhetest",
    "pwd": "123",
    "email": "jincz2000@126.com",
}
register_data1 = {
    "usr": "jinchenzhe",
    "pwd": "123",
    "email": "18307130112@fudan.edu.cn",
}

delete_data = {
    "key": "2021-04-30-124115",
}
def branch1():
    data={
        "email": "18307130112fudan.edu.cn",
    }
    resp = requests.post(local_url + 'login/email_validate', data)
    print(resp)
    cookie = resp.cookies

def branch2():
    data={
        "email": "18307130112fudan.edu.cn",
    }
    resp = requests.post(local_url + 'login/email_validate', data)
    print(resp)
    cookie = resp.cookies

if __name__ == '__main__':
    print("branch1: ")
    branch1()
    print("branch2 ")
    branch2()
