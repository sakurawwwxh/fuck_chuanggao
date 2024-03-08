# -*- coding: utf-8 -*-
from urllib.parse import urlparse, urlencode, quote
from CGEnrypt import get_sign, json_dump
import json
import requests
import time
import Encrypt
import DataManager

# 根url
main_url = 'https://tyapp-scu.chingo.cn/cgapp-server'
# 请求头
org_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-Hans-US;q=1, zh-Hant-US;q=0.9',
    'Connection': 'keep-alive',
    'imei': 'ffffffff-e3ff-eadb-e3ff-eadb00000000',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'cgapp/2.9.8(Linux;Android 13;Xiaomi)',
    'app-key': 'azk3t4jrcfm5772t',  # 这个app-key固定不变
}


def login_req(data, token):
    """用户登录请求"""
    sorted_data = dict(
        sorted(data.items(), key=lambda d: str(d[1]), reverse=True))
    data_str = urlencode(sorted_data)

    login_interface = '/api/f/v6/login'
    full_url = main_url + login_interface
    timestamp = str(int(round(time.time() * 1000)))

    org_headers['Host'] = urlparse(full_url).netloc
    org_headers['sign'] = Encrypt.get_sign(login_interface, data, timestamp)
    org_headers['timestamp'] = timestamp
    org_headers['cgAuthorization'] = token if token else ''

    res = requests.post(full_url, data=data_str, headers=org_headers)
    res.raise_for_status()
    return json.loads(res.text)


def prejudge_req(jsonsports, token, secret):
    interface = '/api/l/v6/prejudgment'
    full_url = main_url + interface
    _, timestamp, _, sign = get_sign(interface, secret, jsonsports)

    org_headers['Host'] = urlparse(full_url).netloc
    org_headers['sign'] = sign
    org_headers['timestamp'] = timestamp
    org_headers['cgAuthorization'] = token if token else ''
    jsonsports_enc = Encrypt.get_enc_pwd(json_dump(jsonsports))
    data = {'jsonsports': quote(jsonsports_enc)}
    # print(jsonsports_enc)
    res = requests.post(full_url, data=data, headers=org_headers)
    return json.loads(res.text)


def prejudge_req_new(jsonsports, token, secret):
    interface = '/api/l/v6.1/prejudgment'
    full_url = main_url + interface
    _, timestamp, _, sign = get_sign(interface, secret, jsonsports)

    org_headers['Host'] = urlparse(full_url).netloc
    org_headers['sign'] = sign
    org_headers['timestamp'] = timestamp
    org_headers['cgAuthorization'] = token if token else ''
    enc_secret = secret[:16].encode()
    jsonsports_enc = Encrypt.aes_encrypt(json_dump(jsonsports), enc_secret)
    data = {'jsonsports': quote(jsonsports_enc)}
    # print(jsonsports_enc)
    res = requests.post(full_url, data=data, headers=org_headers)
    return json.loads(res.text)


def savesports_req(jsonsports, token, secret):
    interface = '/api/l/v7/savesports'
    full_url = main_url + interface
    _, timestamp, _, sign = get_sign(interface, secret, jsonsports)

    org_headers['Host'] = urlparse(full_url).netloc
    org_headers['sign'] = sign
    org_headers['timestamp'] = timestamp
    org_headers['cgAuthorization'] = token if token else ''
    enc_secret = secret[:16].encode()
    jsonsports_enc = Encrypt.aes_encrypt(json_dump(jsonsports), enc_secret)
    data = {'jsonsports': quote(jsonsports_enc)}
    # print(jsonsports_enc)
    res = requests.post(full_url, data=data, headers=org_headers)
    return json.loads(res.text)


def login():
    """登录"""
    user_info = DataManager.get_user_info()

    if 'secret' in user_info and 'token' in user_info:
        print("用户已登录!")
        return user_info

    print("您还未登录, 尝试登录...")
    loginReqBody = {  # provinceCode 根据学校来改
        'username': user_info['account'],
        'password': user_info['password'],
        'provinceCode': 51,  # 四川大学
        'randomCode': 23  # 这个可以随意修改
    }
    loginRes = login_req(loginReqBody, '')
    if 'message' in loginRes:
        msg = loginRes['message']
        if msg == 'OK':
            user_info['name'] = loginRes['data']['info']['xm']
            user_info['uid'] = loginRes['data']['info']['uid']
            user_info['auth'] = loginRes['data']['token']
            auths = user_info['auth'].split('.')
            user_info['token'] = '.'.join(auths[:3])
            user_info['secret'] = auths[3]
            DataManager.save_user_info(user_info)
            print(f"登录成功! 欢迎您, {user_info['name']}同学!")
            return user_info

    print(u'登录失败!', str(loginRes))
    return user_info
