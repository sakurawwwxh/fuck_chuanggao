from datetime import timedelta
from GenerateData import generate_jsonsport
from flask import Flask, render_template, send_from_directory
from flask import session, sessions, jsonify, request
from Encrypt import get_enc_pwd
from DataManager import check_is_valid
import os
import sys
import json
import HttpReq


# Flask Config #
port = 5003
app = Flask(__name__)
app.config['SECRET_KEY'] = "fuckyou_chuanggao"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # cookies在7天后过期


def cglogin(studID, passwd):
    """创高登录"""
    loginReqBody = {  # provinceCode 根据学校来改
        'username': studID,
        'password': get_enc_pwd(passwd),
        'provinceCode': 51,  # 四川大学
        'randomCode': 23  # 这个可以随意修改
    }
    loginRes = HttpReq.login_req(loginReqBody, '')
    user_info = loginReqBody.copy()
    user_info['account'] = studID
    if 'message' in loginRes:
        msg = loginRes['message']
        if msg == 'OK':
            user_info['name'] = loginRes['data']['info']['xm']
            user_info['uid'] = loginRes['data']['info']['uid']
            user_info['auth'] = loginRes['data']['token']
            auths = user_info['auth'].split('.')
            user_info['token'] = '.'.join(auths[:3])
            user_info['secret'] = auths[3]
            print(f"登录成功! 欢迎您, {user_info['name']}同学!")
            return 0, user_info

        if msg == "用户名或密码错误":
            return 1, user_info
    # 未知错误
    return -1, user_info


@app.route('/', methods=["POST", "GET"])
def index():
    # 第2+次进入登陆页面
    # 获取POST请求的参数
    studID = request.form.get("studID")   # 学生证号码
    passwd = request.form.get("passwd")   # 密码
    print("get studID and passwd:", studID, passwd)
    # 用户信息填写完整
    if studID and passwd:
        loginRetCode, user_info = cglogin(studID, passwd)
        if loginRetCode == 0:
            # 登录成功，记住账号密码，user_info
            session['studID'] = studID
            session['passwd'] = passwd
            session['user_info'] = user_info
            return render_template("index.html",
                                   studID=studID,
                                   passwd=passwd,
                                   name=user_info['name'],
                                   loginRetCode=0)
        # 登陆不成功, 但是在cookie中保存了账号密码
        if session.get("studID") is not None and session.get("passwd") is not None:
            return render_template("index.html",
                                   loginRetCode=loginRetCode,
                                   studID=session['studID'],
                                   passwd=session['passwd'])
        # 登陆不成功
        return render_template("index.html", loginRetCode=loginRetCode)
    # 用户没有填写完整, 但是在cookie中保存了账号密码
    if session.get("studID") is not None and session.get("passwd") is not None:
        return render_template("index.html",
                               loginRetCode=2,
                               studID=session['studID'],
                               passwd=session['passwd'])
    # 用户没有填写完整
    return render_template("index.html", loginRetCode=2)


@app.route('/favicon.ico')
def favicon():
    # 设置 favicon 网页图标
    return send_from_directory(
        os.path.join(app.root_path, 'images'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')


@app.route('/run', methods=["POST"])
def run():
    user_info = session.get('user_info')
    if not user_info:
        print("请先登录！")
        return {"code": -1, "message": "请先登录！"}
    data = request.get_json()
    point_list = data["pointList"]
    is_circle = data["isCircle"]
    for i in range(len(point_list)):
        point_list[i] = (point_list[i][1], point_list[i][0])
    print("get points:", point_list)
    prejudge_jsonsports, jsonsports = generate_jsonsport(
        user_info, point_list, is_circle)
    prejudge_resp = HttpReq.prejudge_req_new(
        prejudge_jsonsports, user_info['token'], user_info['secret'])
    print(prejudge_resp)
    if check_is_valid(prejudge_resp):
        print("prejudge 检验成功, 上传数据...")
        savesports_resp = HttpReq.savesports_req(
            jsonsports, user_info['token'], user_info['secret'])
        print(savesports_resp)
        return savesports_resp
        # return jsonify({"code": 200, "message": "成功上传，运动数据审核中"})

    print("prejudge 检验失败")
    return jsonify(prejudge_resp)


if __name__ == '__main__':
    print("runing on server http://localhost:" + str(port))
    app.run(host='0.0.0.0', port=port)
    server.serve_forever()
