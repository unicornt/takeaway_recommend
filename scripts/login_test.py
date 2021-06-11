from collections import defaultdict
from hashlib import sha256

import requests
import xlrd

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
    resp = requests.post(url + 'login/log_in', data)
    cookie = resp.cookies
    print(cookie.items())
    print(resp.json())
    resp = requests.post(url + 'login/log_in', data, cookies=cookie)
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


def readCommentPos(filename):
    file = xlrd.open_workbook(filename).sheet_by_name('Sheet1')
    information = []
    for i in range(1, file.nrows):
        information.append(file.row_values(i))
    return information


def posts(cookie, file, head):
    resp = requests.post(local_url + 'recommend/new_recommend', head, cookies=cookie, files=file)
    print(resp)
    return resp


def doinputrecommend(cookie):
    readInfo = readCommentPos('./menu.xlsx')
    for i, atom in enumerate(readInfo):
        # print(i)
        if atom[0] == 0:
            break
        if i < 0:
            continue
        print(atom)
        head = {
            "title": atom[3],
            "text": (atom[4] + "\n" + atom[11]),
            "timeRange": atom[9],
            "catalog": atom[10],
            "like": int(atom[7]),
            "clicks": int(atom[8]),
            "testflag": 1,
        }
        lens = int(atom[6]) + 1
        files = defaultdict()
        print("A", lens, range(1, lens))
        for i in range(1, lens):
            path = "./picture/{0}-{1}.jpg".format(int(atom[0]), i)
            files[str(i)] = open(path, "rb")
        print(files)
        resp = requests.post(local_url + 'recommend/input_recommend', head, cookies=cookie, files=files)
        print(resp)


if __name__ == '__main__':
    login_logout_test(local_url,register_data1)

