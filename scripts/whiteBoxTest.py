import json
from collections import defaultdict
from time import sleep
import requests

local_url = 'http://localhost:8000/'
remote_url = 'http://45.134.171.215:8000/'
internal_url = 'http://192.168.1.111:8000/'


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
    print(resp.status_code, "此处关注后端输出")
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
    print(resp.status_code, "此处关注后端输出")
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
    code = content['code'] + 'AAA'
    resp = requests.post(local_url + 'login/confirm?code={0}'.format(code))
    print(resp.status_code, "此处关注后端输出")


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
    print(resp.status_code, "此处关注后端输出")


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
    print(resp.status_code, "此处关注后端输出")
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


def logintest():
    print("---------------------logintest---------------------")
    print("branch1: ")
    branch1()
    print("branch2: ")
    branch2()
    print("branch3: ")
    branch3()
    print("branch4: ")
    branch4()
    print("branch5: ")
    branch5()
    print("branch6: ")
    branch6()
    print("branch8: ")
    branch8()
    print("branch9: ")
    branch9()
    print("branch10: ")
    branch10()


def recommend1(cookie, id):
    te = "测试创建推荐{0}".format(id)
    head = {
        "title": te,
        "text": te * 6,
        "timeRange": "早餐",
        "catalog": "火锅",
        "like": 0,
        "clicks": 0,
        "testflag": 1,
    }
    files = defaultdict()
    path = "./testpic.jpg"
    files['1'] = open(path, "rb")
    resp = requests.post(local_url + 'recommend/input_recommend', head, cookies=cookie, files=files)
    print(resp.text)
    return json.loads(resp.text)['content']['key']


def recommend2(key, cookie):
    resp = requests.post(local_url + 'recommend/click/?rid={0}'.format(key), cookies=cookie)
    print(resp.text)


def recommend3(key, type, cookie):
    resp = requests.post(local_url + 'recommend/like/?rid={0}&otype={1}'.format(key, type), cookies=cookie)
    print(resp.text)


def recommend4(key, cookie):
    resp = requests.post(local_url + 'recommend/delete_recommend/?key={0}'.format(key), cookies=cookie)
    print(resp.text)


def recommend5(key, cookie):
    resp = requests.post(local_url + 'recommend/get_recommend/?id={0}'.format(key), cookies=cookie)
    print(resp.text)


def recommend6(cookie):
    resp = requests.post(local_url + 'recommend/all_recommend', cookies=cookie)
    dicts = json.loads(resp.text)['content']
    for key, value in dicts.items():
        print(key, value['user'], value['rid'], value['title'])


def recommend7(cookie):
    body = {
        "username": "jinchenzhetest",
    }
    resp = requests.post(local_url + 'recommend/user_recommend', data=body, cookies=cookie)
    dicts = json.loads(resp.text)['content']
    for key, value in dicts.items():
        print(key, value['user'], value['rid'], value['title'])


def recommend8(cookie):
    body = {
        "username": "jinchenzhetest",
    }
    resp = requests.post(local_url + 'recommend/user_recommend', data=body, cookies=cookie)
    dicts = json.loads(resp.text)['content']
    for key, value in dicts.items():
        print(key, value['user'], value['rid'], value['title'], value['like'])


def recommend9(type, cookie):
    body = {
        "type": type,
        "time": "早餐",
        "upbound": 51,
        "downbound": 0,
    }
    resp = requests.post(local_url + 'recommend/type_recommend', data=body, cookies=cookie)
    dicts = json.loads(resp.text)['content']
    for key, value in dicts.items():
        print(key, value['rid'], value['user'], value['title'], value['timeRange'], value['catalog'])


def recommendtest():
    global key
    print("---------------------recommendtest---------------------")
    data3 = {
        "usr": "jinchenzhetest",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/log_in', data=data3)
    print(resp.text)
    cookie = resp.cookies
    ################################
    print("recommend1: ")
    key = recommend1(cookie, 10085)
    print("recommend2: ")
    recommend2(key, cookie)
    print("recommend3: ")
    recommend3(key, "like", cookie)
    recommend3(key, "like", cookie)
    recommend3(key, "cancel", cookie)
    print("recommend4: ")
    recommend4(key, cookie)
    ################################
    for i in range(5):
        key = recommend1(cookie, i)
        if i % 2 == 0:
            recommend3(key, "like", cookie)
    print("recommend5: ")
    recommend5(key,cookie)
    print("recommend6: ")
    recommend6(cookie)
    print("recommend7: ")
    recommend7(cookie)
    print("recommend8: ")
    recommend8(cookie)
    print("recommend9: ")
    recommend9("timeRange",cookie)
    print("recommend10: ")
    recommend9("catalogRange", cookie)
    print("recommend11: ")
    resp = requests.post(local_url + 'login/log_out', cookies=cookie)
    print(resp.text)
    recommend9("timeRange", cookie)


if __name__ == '__main__':
    logintest()
    recommendtest()
