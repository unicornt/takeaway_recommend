import json
from collections import defaultdict
from time import sleep
import requests

local_url = 'http://localhost:8000/'
remote_url = 'http://45.134.171.215:8000/'
internal_url = 'http://192.168.1.111:8000/'


def branch1():
    print("---------------------branch1---------------------")
    data = {
        "email": "18307130112@fudan.edu.cn",
    }
    resp = requests.post(local_url + 'login/email_validate', data)
    print("注册邮箱\n",resp.text)
    try:
        content = json.loads(resp.text).get('content')
        code = content['code']
        resp = requests.post(local_url + 'login/confirm?code={0}'.format(code))
        print("校对验证码\n",resp.status_code, "此处关注后端输出")
    except:
        print("校对验证码：邮箱已被注册，跳过此步骤")
    data2 = {
        'email': data['email'],
        'usr': "jinchenzhe",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/register', data2)
    print("填写注册信息\n",resp.text)
    resp = requests.post(local_url + 'login/log_in', data=data2)
    print("登录\n",resp.text)
    cookie=resp.cookies

    te = "测试创建推荐branch1"
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
    print("上传推荐\n",resp.text)
    key= json.loads(resp.text)['content']['key']

    for i in range(10):
        resp = requests.post(local_url + 'recommend/click/?rid={0}'.format(key), cookies=cookie)
        print("点击推荐 times:{0}\n".format(i),resp.text)
    for i in range(10):
        resp = requests.post(local_url + 'recommend/like/?rid={0}&otype=like'.format(key), cookies=cookie)
        print("点赞推荐 times:{0}\n".format(i),resp.text)
    for i in range(10):
        resp = requests.post(local_url + 'recommend/like/?rid={0}&otype=cancel'.format(key), cookies=cookie)
        print("取消点赞推荐 times:{0}\n".format(i),resp.text)

    body = {
        "type": type,
        "time": "早餐",
        "upbound": 51,
        "downbound": 0,
    }
    resp = requests.post(local_url + 'recommend/type_recommend', data=body, cookies=cookie)
    dicts = json.loads(resp.text)['content']
    print("返回合适数目推荐\n")
    for key, value in dicts.items():
        print(key, value['rid'], value['user'], value['title'], value['timeRange'], value['catalog'])


    resp = requests.post(local_url + 'login/log_out', cookies=cookie)
    print("登出\n",resp.text)

def branch2():
    print("---------------------branch2---------------------")
    data2 = {
        'email': "1007552535@qq.com",
        'usr': "jinchenzhe"*10,
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/register', data2)
    print("填写注册信息\n",resp.text)
    data3={
        'usr': "jinchenzhetest",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/log_in', data=data3)
    print("登录\n",resp.text)
    cookie=resp.cookies

    body = {
        "type": type,
        "time": "早餐",
        "upbound": -1,
        "downbound": 0,
    }
    resp = requests.post(local_url + 'recommend/type_recommend', data=body, cookies=cookie)
    dicts = json.loads(resp.text)['content']
    print("返回0数目推荐\n")
    for key, value in dicts.items():
        print(key, value['rid'], value['user'], value['title'], value['timeRange'], value['catalog'])
    resp = requests.post(local_url + 'login/log_out', cookies=cookie)
    print("登出\n",resp.text)

def branch3():
    print("---------------------branch3---------------------")
    data2 = {
        'email': "1007552535@qq.com",
        'usr': "",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/register', data2)
    print("填写注册信息\n",resp.text)
    data3={
        'usr': "jinchenzhetest",
        'pwd': '123',
    }
    resp = requests.post(local_url + 'login/log_in', data=data3)
    print("登录\n",resp.text)
    cookie=resp.cookies

    body = {
        "type": type,
        "time": "早餐",
        "upbound": 1000,
        "downbound": -10,
    }
    resp = requests.post(local_url + 'recommend/type_recommend', data=body, cookies=cookie)
    dicts = json.loads(resp.text)['content']
    print("返回1010数目推荐\n总返回输入数：{0}\n".format(len(dicts)))
    for key, value in dicts.items():
        print(key, value['rid'], value['user'], value['title'], value['timeRange'], value['catalog'])
    resp = requests.post(local_url + 'login/log_out', cookies=cookie)
    print("登出\n",resp.text)

if __name__ == '__main__':
    branch1()
    # branch2()
    # branch3()
