# -*- coding: utf-8 -*-
import HttpReq
from DataManager import check_is_valid
from GenerateData import generate_jsonsport


def main():
    user_info = HttpReq.login()
    print("开始运动!")
    prejudge_jsonsports, jsonsports = generate_jsonsport(None)
    prejudge_resp = HttpReq.prejudge_req_new(
        prejudge_jsonsports, user_info['token'], user_info['secret'])
    print(prejudge_resp)
    if check_is_valid(prejudge_resp):
        print("prejudge 检验成功, 上传数据...")
        if input("确定上传吗？y:上传;n:取消：") == "y":
            savesports_resp = HttpReq.savesports_req(
                jsonsports, user_info['token'], user_info['secret'])
            print(savesports_resp)


if __name__ == '__main__':
    main()
