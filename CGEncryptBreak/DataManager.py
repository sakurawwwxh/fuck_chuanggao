# -*- coding: utf-8 -*-
import os
import Encrypt
import json


def check_is_valid(resp):
    if resp['code'] != 200:
        return False
    if resp['message'] != 'OK':
        return False
    for d in resp['data']:
        if d['isvalid'] != '1':
            print("失败：", d['content'])
            return False
    return True


def get_user_input():
    """获取用户输入搜索条件"""
    account = input('请输入账号: ')
    password = input('请输入密码: ')
    # AES加密password
    password = Encrypt.get_enc_pwd(password)
    return {'account': account, 'password': password}


def get_user_info():
    """检测目录中是否存在用户信息的JSON文件"""
    current_directory = os.path.dirname(os.path.realpath(__file__))
    user_info_file = os.path.join(current_directory, 'user_info.json')

    if os.path.exists(user_info_file):
        with open(user_info_file, 'r') as file:
            user_info = json.load(file)
            if user_info:
                print("检测到已保存的用户信息")
                # print(user_info)
                return user_info
            print("用户信息为空, 需要更新")
            user_info = get_user_input()
            save_user_info(user_info)
            return user_info
    print("未找到用户信息文件, 需要获取用户信息")
    user_info = get_user_input()
    save_user_info(user_info)
    return user_info


def save_user_info(user_info):
    """保存用户信息到JSON文件, 保存到directory目录下"""
    current_directory = os.path.dirname(os.path.realpath(__file__))
    user_info_file = os.path.join(current_directory, 'user_info.json')
    with open(user_info_file, 'w') as file:
        json.dump(user_info, file)
        print("登录信息已保存到文件：", user_info_file)
