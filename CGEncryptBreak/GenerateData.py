# -*- coding: utf-8 -*-
import DataManager
import math
import random
import uuid
import json
import time
import datetime
# 用于计算地球球面两点之间的距离
from geopy.distance import geodesic

"""
二号运动场坐标: (逆时针) 纬度, 经度
p1: (30.557034,104.005777).(30.557108,104.005831) -> (30.557071,104.005804)
p2: (30.555866,104.006818).(30.555935,104.00685) -> (30.5559005,104.006834)
p3: (30.556526,104.007821).(30.556623,104.00789) -> (30.5565745,104.0078555)
p4: (30.557713,104.006802).(30.557778,104.006861) -> (30.5577455,104.0068315)
"""
default_point_list = [
    (30.557071, 104.005804), (30.5559005, 104.006834),
    (30.5565745, 104.0078555), (30.5577455, 104.0068315),
]

jsonsport_template = {
    "activeTime": "",  # 跑步总耗时
    "alreadyPassPoint": "",
    "alreadyPassPointResult": "",
    "avgPace": "",  # 每公里平均用时 (21*60+46)/3.09 -> 7'03''
    "avgSpeed": "",  # 平均速度 (km/h) (3.09/(21*60+46)*60*60)
    "beganPoint": "",  # 起始坐标
    "beginTime": "",  # 起始时间
    "calorie": 0,  # 消耗卡路里 (暂时按Calorie=57.0949*odometer−1.1293)
    "coordinate": [
        {
            "a": 0.0,  # 纬度 l"a"titude (GCJ02坐标系)
            "ac": 0.0,  # GPS定位精度, 单位(米), 越小越精确
            "d": 0.0,  # distance, 跑步距离
            "da": 0.0,  # distance all, 跑步总距离
            "o": 0.0,  # 经度 l"o"ngitude (GCJ02坐标系)
            "s": 0.0,  # speed 速度, 计算方式未知, 可能是直接调用传感器
            "st": 0,  # step, 上一步步数, 一般为 0
            "sta": 0,  # step all, 总步数, 一般为 0
            "t": 0,  # timestamp 时间戳
            "v": 0  # valid, 一般为 1
        }
    ],
    "endPoint": "",  # 终止坐标
    "endTime": "",  # 终止时间
    "indoor": 0,  # 是否在室内
    "isValid": 1,  # 是否计入
    "isValidReason": "",  # 跑步不成功的原因
    "lastOdometerTime": "",  # 最后不到一公里的用时
    "maxSpeedPerHour": "",  # 最高时速, 计算方式未知
    "minSpeedPerHour": "",  # 最低时速, 计算方式未知
    "minuteSpeed": [  # 每分钟内的平均速度
        {
            "min": "",  # 第几分钟
            "v": ""  # 这一分钟内的平均速度
        }
    ],
    "modementMode": "",  # 未知
    "name": "",  # 姓名
    "needPassPointCount": "",  # 需要经过的点位 (一般为0)
    "odometer": "",  # 运动总路程 = (d[-1]+da[-1])/1000 (km)
    "pace": [  # 每公里平均用时
        {
            "km": "1",
            "t": "00\u002700\u0027\u0027"
        },
        {
            "km": "2",
            "t": "00\u002700\u0027\u0027"
        },
        {
            "km": "3",
            "t": "00\u002700\u0027\u0027"
        }
    ],
    "phoneVersion": "",  # 手机型号+创高体育版本
    "planRouteName": "",  # 线路名称
    "routeId": "",  # 线路ID
    "sportId": "",  # 暂定为随机生成UUID
    "stepCount": 0,  # 实测是根据传感器得出的, 正常为 总距离/步幅 = 3090m/1.5m
    "stepMinute": "",  # 每分钟步数 = 步数/秒数×60 | 步频应当在170-180步/分更合理
    "xh": ""  # 学号
}


def generate_sportId():
    return str(uuid.uuid4())


def milliseconds_to_time(milliseconds):
    seconds = milliseconds // 1000
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    time_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

    return time_str


def generate_GPS_accuracy():
    """
    生成 coordinate.ac
    GPS精度等级, 单位m, 越小说明定位越准确
    """
    def gaussian_pdf(x, mean, std_dev):
        """高斯分布概率密度函数"""
        exponent = math.exp(-(math.pow(x-mean, 2) / (2*math.pow(std_dev, 2))))
        return (1 / (math.sqrt(2*math.pi) * std_dev)) * exponent

    def select_from_array(arr):
        """根据高斯分布的概率从数组中选择一个元素"""
        mean = len(arr) / 2  # 计算数组的中点
        std_dev = len(arr) / 4  # 计算标准差, 这里我们使用数组长度的四分之一作为标准差
        probabilities = [gaussian_pdf(x, mean, std_dev) for x in arr]
        # 归一化概率, 使其总和为1
        probabilities = [p / sum(probabilities) for p in probabilities]
        rand, total = random.random(), 0
        for i, p in enumerate(probabilities):
            total += p
            if rand < total:
                return arr[i]

    ac_list = [
        # 2.200000047683716,
        2.0999999046325684,
        2.0,
        1.899999976158142,
        1.7999999523162842,
        1.7000000476837158,
        1.600000023841858,
        1.5,
        1.399999976158142,
        1.2000000476837158,
        1.100000023841858,
    ]

    return select_from_array(ac_list)


def pos2string(pos_a, pos_o):
    return f"{pos_a}|{pos_o}"


def timestamp2string(timestamp):
    timestamp = timestamp / 1000  # 将毫秒级时间戳转换为秒级时间戳
    # 将时间戳转换为日期时间对象
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    # 将日期时间对象格式化为指定的字符串格式
    formatted_date_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    # print(formatted_date_time)
    return formatted_date_time


def generate_random_position(pos_a, pos_o, diff_a, diff_o):
    rand_pos_a = pos_a + (1 - random.random() * 2) * diff_a
    rand_pos_o = pos_o + (1 - random.random() * 2) * diff_o
    # print("random_position:", round(rand_pos_a, 6), round(rand_pos_o, 6))
    return round(rand_pos_a, 6), round(rand_pos_o, 6)  # 保留6位小数


def generate_jsonsport(user_info, point_list=default_point_list, is_circle=True):
    """生成用于/api/l/v7/savesports接口的随机数据"""
    jsonsport = jsonsport_template.copy()

    if user_info is None:
        user_info = DataManager.get_user_info()

    # ############# 固定参数 ############# #
    jsonsport['name'] = user_info['name']  # 姓名
    jsonsport['xh'] = user_info['account']  # 账号（学号）
    """
    江安校区-男生 24
    华西校区足球场-男 38
    华西校区田径场-男生 29
    江安校区2号运动场-男生 27
    望江体育中心-男生 31
    望江东区田径场-男生 33
    """
    jsonsport['routeId'] = "24"  # 线路选择
    jsonsport['planRouteName'] = "江安校区"  # 线路名称
    jsonsport['phoneVersion'] = "23078RKD5C,33,13|2.9.8"  # 手机型号+创高体育版本
    jsonsport['sportId'] = generate_sportId()  # sportId 应不重复
    jsonsport['modementMode'] = "2"
    jsonsport['needPassPointCount'] = "0"  # 需要经过的点位 (一般为0)
    jsonsport['isValid'] = 1  # 是否计入
    jsonsport['isValidReason'] = ""  # 跑步不成功的原因
    jsonsport['indoor'] = 0  # 是否在室内
    jsonsport['alreadyPassPoint'] = ""
    jsonsport['alreadyPassPointResult'] = ""
    jsonsport['minuteSpeed'] = []  # 每分钟内的平均速度
    jsonsport['pace'] = []  # 每公里平均用时

    # ############# 动态参数 ############# #
    pace = [0]  # pace[n] 指的是第n公里结束时花的时间
    minu_dis = [0]  # mimu_dis[n] 指的是第n分钟结束时跑完的路程
    if is_circle:  # 循环跑100圈总归有3公里了吧？
        point_list = point_list * 100
    began_point = generate_random_position(*point_list[0], 0.000032, 0.000016)
    end_point = generate_random_position(*point_list[-1], 0.000032, 0.000016)
    # 按时间先后: 开始 -> 3s后 -> 记录运动 -> 结束运动 -> 3s后(网络延迟) -> 提交
    start_time = begin_time = end_time = submit_time = 0
    distance_all = distance = 0
    minute_cnt = time_all = pp_time = 0
    max_speed, min_speed = -1, 1e10
    last_point = began_point  # 上一个坐标
    jsonsport['coordinate'] = [
        {
            "a": began_point[0],  # 纬度 l"a"titude (GCJ02坐标系)
            "ac": 0.0,  # GPS定位精度, 单位(米), 越小越精确
            "d": distance,  # distance, 跑步距离
            "da": distance_all,  # distance all, 跑步总距离
            "o": began_point[1],  # 经度 l"o"ngitude (GCJ02坐标系)
            "s": 0.0,  # speed 速度, 计算方式未知, 可能是直接调用传感器
            "st": 0,  # 未知, 一般为 0
            "sta": 0,  # 未知, 一般为 0
            "t": 0,  # timestamp 时间戳
            "v": 0  # valid, 一般为 1
        }
    ]
    # 提前算好大概要跑多少 (粗略估计) [3.02, 3.52] 之间
    rough_odometer = 3.02 + random.random() / 2
    print("我想跑", rough_odometer, "公里")
    finished = False  # 是否已经跑完了
    for i in range(len(point_list) - 1):
        if finished:
            break
        # rough_speed = rough_odometer * 2.7  # 保证跑大约20分钟
        rough_speed = 9 + random.random()  # 慢跑最佳速度 10km/h, 6min/km
        # 计算与下一个点之间的距离, 距离单位为米
        pp_distance = geodesic(point_list[i], point_list[i + 1]).meters
        # 如果按照speed跑的话, 需要大概分割成多少段 (每段~2 second)
        # point_count = pp_distance / (rough_speed / 3.6) / 2
        point_count = int(pp_distance / rough_speed * 1.8)
        if point_count == 0:
            point_count = 1  # 防止 ZeroDivisionError: float division by zero
        # 计算每两点之间的经纬度间隔
        delta_a = (point_list[i + 1][0] - point_list[i][0]) / point_count
        delta_o = (point_list[i + 1][1] - point_list[i][1]) / point_count
        for j in range(int(point_count)):
            rand_point = generate_random_position(
                point_list[i][0] + delta_a * j,
                point_list[i][1] + delta_o * j,
                0.000004, 0.000004)  # xy偏移量: 0.629m
            pp_time = 2000 - random.randint(0, 5)  # 单位: ms
            time_all += pp_time  # 累加跑步总时间
            distance = geodesic(rand_point, last_point).meters
            distance_all += distance  # 累加跑步总距离
            speed = distance / pp_time * 1000 * 3.6  # 速度 (km/h)
            if speed > max_speed:
                max_speed = speed
            if speed < min_speed:
                min_speed = speed
            jsonsport['coordinate'].append({
                "a": rand_point[0],  # 纬度 l"a"titude (GCJ02坐标系)
                "ac": generate_GPS_accuracy(),  # GPS定位精度, 单位(米), 越小越精确
                "d": distance,  # distance, 跑步距离
                "da": distance_all,  # distance all, 跑步总距离
                "o": rand_point[1],  # 经度 l"o"ngitude (GCJ02坐标系)
                "s": round(speed, 2),  # speed 速度
                "st": 0,  # 未知, 一般为 0
                "sta": 0,  # 未知, 一般为 0
                "t": pp_time,  # 需要后期转化为 timestamp 时间戳
                "v": 1  # valid, 一般为 1
            })
            km_count = int(distance_all / 1000) + 1  # 现在是第几公里
            minute_cnt = int(time_all / 60000) + 1  # 现在是第几分钟
            if km_count >= len(pace):
                pace.append(0)
            if minute_cnt >= len(minu_dis):
                minu_dis.append(0)
            pace[km_count] = time_all  # 单位: ms
            minu_dis[minute_cnt] = int(distance_all)  # 单位: m
            last_point = rand_point
            if is_circle and distance_all >= rough_odometer * 1000:  # 跑完了
                finished = True
                end_point = rand_point
                submit_time = round(time.time() * 1000)
                # 减掉网络延迟产生的时间误差
                end_time = submit_time - round(random.random() * 3000)
                begin_time = end_time - time_all
                # 减掉开始时的倒计时 (3s)
                start_time = begin_time - 3000
                break
    # 路线都结束了还没跑完, 只能强行结束了
    if not finished:
        end_point = rand_point
        submit_time = round(time.time() * 1000)
        # 减掉网络延迟产生的时间误差
        end_time = submit_time - round(random.random() * 3000)
        begin_time = end_time - time_all
        # 减掉开始时的倒计时 (3s)
        start_time = begin_time - 3000

    # 运动总路程
    odometer = (distance + distance_all) / 1000  # 不知道为啥这么算, 创高的bug
    jsonsport['odometer'] = f"{round(odometer, 2):.2f}"  # 精确到小数点后两位
    # 起止时间
    jsonsport['beginTime'] = timestamp2string(start_time)
    jsonsport['endTime'] = timestamp2string(submit_time)
    # 起止点
    jsonsport['beganPoint'] = pos2string(*began_point)
    jsonsport['endPoint'] = pos2string(*end_point)
    # 拟合出来的卡路里计算公式
    jsonsport['calorie'] = round(57.0949 * odometer - 1.1293, 1)
    # 步幅 & 步数 & 每分钟步数
    step_length = 2 + random.random() * 0.2  # 正常人跑步步幅在1米~1.2米左右
    jsonsport['stepCount'] = round(odometer * 1000 / step_length)
    # 实测，stepMinute >= 100 时很容易报参数错误
    jsonsport['stepMinute'] = str(round(
        jsonsport['stepCount'] / (time_all // 1000) * 60, 2))
    # 最大最小时速
    jsonsport['maxSpeedPerHour'] = str(round(max_speed, 2))
    jsonsport['minSpeedPerHour'] = str(round(min_speed, 2))
    # 总耗时 和 最后不到一公里耗时
    jsonsport["activeTime"] = milliseconds_to_time(time_all)
    jsonsport['lastOdometerTime'] = milliseconds_to_time(pace[-1] - pace[-2])
    # 每公里平均用时 和 平均速度
    seconds = round((time_all // 1000) / odometer)
    minute = str(seconds // 60).zfill(2)
    second = str(seconds % 60).zfill(2)
    jsonsport["avgPace"] = f"{minute}\u0027{second}\u0027\u0027"
    jsonsport["avgSpeed"] = str(round(odometer / (time_all // 1000) * 3600, 1))
    # 将时间间隔转化为 timestamp 时间戳
    for p in jsonsport['coordinate']:
        begin_time += p['t']
        p['t'] = begin_time
    jsonsport['coordinate'][0]['t'] = 0  # 起点没有timestamp
    # 计算每公里平均用时, k=1,2,3...len(pace)-2
    for k in range(1, len(pace) - 1):
        killo_seconds = (pace[k] - pace[k - 1]) // 1000
        minute = str(killo_seconds // 60).zfill(2)
        second = str(killo_seconds % 60).zfill(2)
        jsonsport['pace'].append({
            "km": str(k),  # 第几公里
            "t": f"{minute}\u0027{second}\u0027\u0027"
        })
    # 计算每分钟内的平均速度, 最后一分钟不需要上传
    for m in range(1, minute_cnt):
        # 计算每分钟的 speed, 这里一分钟按60秒算, 有误差不管了
        s = (minu_dis[m] - minu_dis[m - 1]) * 0.06
        jsonsport['minuteSpeed'].append({
            "min": str(m),  # 第几分钟
            "v": str(round(s, 2))
        })
    # print("pace:", pace)
    # print("minute_dis:", minu_dis)

    # 计算上传到 prejudgement 的 jsonsports, 少几个参数
    prejudge_jsonsport = jsonsport.copy()
    prejudge_jsonsport.pop("coordinate", None)
    prejudge_jsonsport.pop("beganPoint", None)
    prejudge_jsonsport.pop("endPoint", None)
    for i, ms in enumerate(prejudge_jsonsport['minuteSpeed']):
        ms["baseObjId"] = 63 + i
    for i, p in enumerate(prejudge_jsonsport['pace']):
        p["baseObjId"] = 8 + i
    return prejudge_jsonsport, jsonsport


if __name__ == '__main__':
    print(json.dumps(generate_jsonsport(None)[1]))
