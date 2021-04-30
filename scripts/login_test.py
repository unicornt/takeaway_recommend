from hashlib import sha256

import requests

local_url = 'http://localhost:8000/'
remote_url = 'http://45.134.171.215:8000/'
internal_url = 'http://192.168.1.111:8000/'

register_data2 = {
    'usr': '1111111',
    'pwd': '12345678',
    'email': '18307130112@fudan.edu.cn',
}
register_data3 = {
    'usr': '11111112',
    'pwd': '1234567',
    'email': '18307130112@fudan.edu.cn',
}
change_data1 = {
    'usr': '1111111',
    'old_pwd': '1234567',
    'new_pwd': '1234567',
    'email': '18307130112@fudan.edu.cn',
}
change_data2 = {
    'usr': '1111111',
    'old_pwd': '1234567',
    'new_pwd': '12345678',
    'email': '18307130112@fudan.edu.cn'
}
change_data3 = {
    'usr': '1111111',
    'old_pwd': '12345678',
    'new_pwd': '1234567',
    'email': '18307130112@fudan.edu.cn'
}

login_data1 = {
    'usr': '1111111',
    'pwd': '1234567',
}
login_data2 = {
    'usr': '18307130112@fudan.edu.cn',
    'pwd': '1234567',
}


def hash_code(s, salt='users_hash'):
    h = sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def register_test(url, data):
    print('register_test:')
    resp = requests.post(url + 'login/register', json=data)
    print(resp.json())


def login_test(url, data):
    print('login_test:')
    resp = requests.post(url + 'login/log_in', json=data)
    print(resp.json())


def email_validate_test(url, data):
    print('email_validate_test:')
    resp = requests.post(url + 'login/email_validate', json=data)
    print(resp.json())


def reset_pwd_test(url, data):
    print('reset_pwd_test:')
    resp = requests.post(url + 'login/reset_pwd', json=data)
    print(resp.json())


def change_pwd_test(url, data):
    print('change_pwd_test:')
    resp = requests.post(url + 'login/log_in', json=data)
    print(resp.json())
    cookie = resp.cookies
    print(cookie.items())
    resp = requests.post(url + 'login/change_pwd', json=change_data1, cookies=cookie)
    print(resp.json())
    resp = requests.post(url + 'login/change_pwd', json=change_data2, cookies=cookie)
    print(resp.json())
    resp = requests.post(url + 'login/change_pwd', json=change_data3, cookies=cookie)
    print(resp.json())


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


register_data1 = {
    "usr": "jinchenzhe",
    "pwd": "123",
    "email": "18307130112@fudan.edu.cn",
}
delete_data = {
    "key": "2021-04-30-124115",
}
if __name__ == '__main__':
    resp = requests.post(local_url + 'login/log_in', register_data1)
    cookie = resp.cookies
    resp=requests.post(local_url+'recommend/delete_recommend/',delete_data,cookies=cookie)
    # login_logout_test(local_url,register_data1)
    # data = {
    #     'type': '0',
    #     'user': 'unicornt',
    #     'upbound': '3',
    #     'downbound': '2',
    #     'order': '-',
    # }
    # print(data)
    # requests.post(local_url + 'recommend/get_recommends',
    #               {
    #                   'type': '2',
    #                   'user': 'unicornt',
    #                   'upbound': '3',
    #                   'downbound': '2',
    #                   'order': '+',
    #               })
    # get_place_device_test(local_url)

    # print(hash_code('1234567'))
    # asset_test(internal_url)
    # register_test(local_url, register_data1)
    # register_test(local_url, register_data2)
    # register_test(local_url, register_data3)
    # login_logout_test(local_url,login_data2)
    # email_validate_test(local_url, register_data1)
    # change_pwd_test(local_url,register_data2)
    # reset_pwd_test(local_url, register_data1)

    # register_test(local_url, register_data1)
    # reset_pwd_test(local_url, register_data1)
    # login_data3 = {
    #     'usr': '18307130112@fudan.edu.cn',
    #     'pwd': 'f5c9b48194669179',
    # }
    # change_data4 = {
    #     'usr': '1111111',
    #     'old_pwd': 'f5c9b48194669179',
    #     'new_pwd': '1234567',
    #     'email': '18307130112@fudan.edu.cn'
    # }
    # resp = requests.post(local_url + 'login/log_in', json=login_data3)
    # print(resp.json())
    # cookie = resp.cookies
    # print(cookie.items())
    # resp = requests.post(local_url + 'login/change_pwd', json=change_data4, cookies=cookie)
    # print(resp.json())
