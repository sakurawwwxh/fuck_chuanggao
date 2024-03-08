# -*- coding: utf-8 -*-
import HttpReq
from DataManager import check_is_valid
from GenerateData import generate_jsonsport

success_data = {
    "activeTime": "00:19:28",
    "alreadyPassPoint": "",
    "alreadyPassPointResult": "",
    "avgPace": "06'01''",
    "avgSpeed": "10.0",
    "beginTime": "2024-03-06 22:49:33",
    "calorie": 183.6,
    "endTime": "2024-03-06 23:09:06",
    "indoor": 0,
    "isValid": 1,
    "isValidReason": "",
    "lastOdometerTime": "00:01:25",
    "maxSpeedPerHour": "19.62",
    "minSpeedPerHour": "1.41",
    "minuteSpeed": [
        {
            "min": "1",
            "v": "10.21",
            "baseObjId": 63
        },
        {
            "min": "2",
            "v": "10.33",
            "baseObjId": 64
        },
        {
            "min": "3",
            "v": "9.73",
            "baseObjId": 65
        },
        {
            "min": "4",
            "v": "10.15",
            "baseObjId": 66
        },
        {
            "min": "5",
            "v": "10.1",
            "baseObjId": 67
        },
        {
            "min": "6",
            "v": "10.27",
            "baseObjId": 68
        },
        {
            "min": "7",
            "v": "9.85",
            "baseObjId": 69
        },
        {
            "min": "8",
            "v": "9.91",
            "baseObjId": 70
        },
        {
            "min": "9",
            "v": "9.67",
            "baseObjId": 71
        },
        {
            "min": "10",
            "v": "9.43",
            "baseObjId": 72
        },
        {
            "min": "11",
            "v": "10.03",
            "baseObjId": 73
        },
        {
            "min": "12",
            "v": "9.55",
            "baseObjId": 74
        },
        {
            "min": "13",
            "v": "9.61",
            "baseObjId": 75
        },
        {
            "min": "14",
            "v": "9.97",
            "baseObjId": 76
        },
        {
            "min": "15",
            "v": "10.45",
            "baseObjId": 77
        },
        {
            "min": "16",
            "v": "10.33",
            "baseObjId": 78
        },
        {
            "min": "17",
            "v": "9.79",
            "baseObjId": 79
        },
        {
            "min": "18",
            "v": "9.97",
            "baseObjId": 80
        },
        {
            "min": "19",
            "v": "9.55",
            "baseObjId": 81
        }
    ],
    "modementMode": "2",
    "name": "\u80e1\u5b97\u5c27",
    "needPassPointCount": "0",
    "odometer": "3.24",
    "pace": [
        {
            "km": "1",
            "t": "05'53''",
            "baseObjId": 8
        },
        {
            "km": "2",
            "t": "06'09''",
            "baseObjId": 9
        },
        {
            "km": "3",
            "t": "05'59''",
            "baseObjId": 10
        }
    ],
    "phoneVersion": "23078RKD5C,33,13|2.9.8",
    "planRouteName": "\u6c5f\u5b89\u6821\u533a",
    "routeId": "24",
    "sportId": "c7f1f87e-5186-4eb1-9ac8-71efe8046c92",
    "stepCount": 2001,
    "stepMinute": "66.99",
    "xh": "2022181640245"
}


def main():
    user_info = HttpReq.login()
    print("开始运动!")
    # prejudge_jsonsports, jsonsports = generate_jsonsport()
    prejudge_jsonsports = success_data
    prejudge_resp = HttpReq.prejudge_req_new(
        prejudge_jsonsports, user_info['token'], user_info['secret'])
    print(prejudge_resp)
    if check_is_valid(prejudge_resp):
        print("prejudge 检验成功, 上传数据...")
        # savesports_resp = HttpReq.savesports_req(
        #     jsonsports, user_info['token'], user_info['secret'])
        # print(savesports_resp)


if __name__ == '__main__':
    main()
