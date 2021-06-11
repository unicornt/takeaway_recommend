import json
from collections import defaultdict
from time import sleep
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
    data = {
        "email": "18307130112fudan.edu.cn",
    }
    resp = requests.post(local_url + 'login/email_validate', data)
    print(resp.text)


def branch2():
    data = {
        "email": "jincz2000@126.com",
    }
    resp = requests.post(local_url + 'login/email_validate', data)
    print(resp.text)


def branch3():
    data = {
        "email": "18307130112@fudan.edu.cn",
    }
    resp = requests.post(local_url + 'login/email_validate', data)
    print(resp.text)
    content = json.loads(resp.text).get('content')
    code = content['code']
    resp = requests.post(local_url + 'login/confirm?code={0}'.format(code))
    print(resp.status_code,"此处关注后端输出")
    data2 = {
        'email': data['email'],
        'usr': "aaaaasssssdddddfffffggggg",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/register', data2)
    print(resp.text)

def branch4():
    data = {
        "email": "18307130112@fudan.edu.cn",
    }
    resp = requests.post(local_url + 'login/email_validate', data)
    print(resp.text)
    content = json.loads(resp.text).get('content')
    code = content['code']
    resp = requests.post(local_url + 'login/confirm?code={0}'.format(code))
    print(resp.status_code,"此处关注后端输出")
    data2 = {
        'email': data['email'],
        'usr': "jinchenzhetest",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/register', data2)
    print(resp.text)

def branch5():
    data = {
        "email": "18307130112@fudan.edu.cn",
    }
    resp = requests.post(local_url + 'login/email_validate', data)
    print(resp.text)
    content = json.loads(resp.text).get('content')
    code = content['code']+'AAA'
    resp = requests.post(local_url + 'login/confirm?code={0}'.format(code))
    print(resp.status_code,"此处关注后端输出")


def branch6():
    '''
    以下测试在调整链接过时时间为5s后执行
    '''
    data = {
        "email": "18307130112@fudan.edu.cn",
    }
    resp = requests.post(local_url + 'login/email_validate', data)
    print(resp.text)
    content = json.loads(resp.text).get('content')
    code = content['code']
    sleep(20)
    resp = requests.post(local_url + 'login/confirm?code={0}'.format(code))
    print(resp.status_code,"此处关注后端输出")


def branch7():
    data = {
        'usr': "18307130112@fudan.edu.cn",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/log_in', data)
    print(resp.text)


def branch8():
    data = {
        'usr': "jinchenzhe",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/log_in', data)
    print(resp.text)


def branch9():
    data = {
        "usr": "jincz2000@126.com",
        'pwd': '1234',
    }
    resp = requests.post(local_url + 'login/log_in', data)
    print(resp.text)


def branch10():
    data = {
        "email": "18307130112@fudan.edu.cn",
    }
    resp = requests.post(local_url + 'login/email_validate', data)
    print(resp.text)
    content = json.loads(resp.text).get('content')
    code = content['code']
    resp = requests.post(local_url + 'login/confirm?code={0}'.format(code))
    print(resp.status_code,"此处关注后端输出")
    data2 = {
        'email': data['email'],
        'usr': "jinchenzhe",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/register', data2)
    print(resp.text)
    data3 = {
        "usr": "jinchenzhe",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/log_in', data=data3)
    print(resp.text)
    cookie = resp.cookies
    resp = requests.post(local_url + 'login/log_out', cookies=cookie)
    print(resp.text)

def branch11():
    data = {
        "email": "1007552535@qq.com",
    }
    resp = requests.post(local_url + 'login/email_validate', data)
    print(resp.text)
    content = json.loads(resp.text).get('content')
    code = content['code']
    resp = requests.post(local_url + 'login/confirm?code={0}'.format(code))
    print(resp.status_code,"此处关注后端输出")
    data2 = {
        'email': data['email'],
        'usr': "jinchenzhe2",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/register', data2)
    print(resp.text)
    data3 = {
        "usr": "1007552535@qq.com",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/log_in', data=data3)
    print(resp.text)
    cookie = resp.cookies
    resp = requests.post(local_url + 'login/log_out', cookies=cookie)
    print(resp.text)


def logintest():
    print("---------------------logintest---------------------")
    # print("branch1: ")
    # branch1()
    # print("branch2: ")
    # branch2()
    # print("branch3: ")
    # branch3()
    # print("branch4: ")
    # branch4()
    # print("branch5: ")
    # branch5()
    # print("branch6: ")
    # branch6()
    # print("branch7: ")
    # branch7()
    # print("branch8: ")
    # branch8()
    # print("branch9: ")
    # branch9()
    print("branch10: ")
    branch10()
    print("branch11: ")
    branch11()

def recommend1():
    data3 = {
        "usr": "jinchenzhetest",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/log_in', data3)
    cookie=resp.cookies
    print(resp.text,cookie.items())

def recommendtest():
    print("---------------------recommendtest---------------------")
    print("recommend1: ")
    recommend1()

if __name__ == '__main__':
    logintest()
    #recommendtest()