from datetime import timedelta
from GenerateData import generate_jsonsport
from flask import Flask, request, render_template, jsonify
import os
import sys
import json
import HttpReq
import requests
import DataManager


# Flask Config #
port = 5003
app = Flask(__name__)
app.config['SECRET_KEY'] = "abcdefghijklmn"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # cookies在7天后过期


def cookieToStr(cookies):
    # 使用utils.dict_from_cookiejar 将cookies数据类型转化为字典
    cookies_dict = requests.utils.dict_from_cookiejar(cookies)
    # 再使用 json.dumps 将字典转化为str字符串
    cookies_str = json.dumps(cookies_dict)
    return cookies_str


def strToCookie(cookies_str):
    # 使用json的loads函数，把str转化为字典。这里需要注意是loads，不是load
    cookies_dict = json.loads(cookies_str)
    # 再将字典恢复成原来的cookies
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)
    return cookies


@app.route('/', methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route('/run', methods=["POST"])
def run():
    user_info = HttpReq.login()
    data = request.get_json()
    point_list = data["pointList"]
    is_circle = data["isCircle"]
    if is_circle:
        point_list.pop()
    for i in range(len(point_list)):
        point_list[i] = (point_list[i][1], point_list[i][0])
    print("get points:", point_list)
    prejudge_jsonsports, jsonsports = generate_jsonsport(point_list, is_circle)
    prejudge_resp = HttpReq.prejudge_req_new(
        prejudge_jsonsports, user_info['token'], user_info['secret'])
    print(prejudge_resp)
    if DataManager.check_is_valid(prejudge_resp):
        print("prejudge 检验成功, 上传数据...")
        # savesports_resp = HttpReq.savesports_req(
        #     jsonsports, user_info['token'], user_info['secret'])
        # print(savesports_resp)
        # return savesports_resp

    return {"code": 400, "msg": "prejudge 检验失败"}


if __name__ == '__main__':
    print("runing on server http://localhost:" + str(port))
    app.run(host='0.0.0.0', port=port)
    server.serve_forever()
