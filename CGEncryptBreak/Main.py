# -*- coding: utf-8 -*-
import HttpReq
import DataManager
from GenerateData import generate_jsonsport


def main():
    while True:
        user_info = HttpReq.login()
        print("开始运动!")
        prejudge_jsonsports, jsonsports = generate_jsonsport(None)
        prejudge_resp = HttpReq.prejudge_req_new(
            prejudge_jsonsports, user_info['token'], user_info['secret'])
        print(prejudge_resp)
        if DataManager.check_is_valid(prejudge_resp):
            print("prejudge 检验成功, 上传数据...")
            if input("确定上传吗？y:上传;n:取消：") == "y":
                savesports_resp = HttpReq.savesports_req(
                    jsonsports, user_info['token'], user_info['secret'])
                print(savesports_resp)
                return savesports_resp
        elif prejudge_resp['code'] == 2001:
            # 登录过期，请重新登录
            print("登录已过期，正在重新登录")
            DataManager.save_user_info({})
            continue


if __name__ == '__main__':
    main()
