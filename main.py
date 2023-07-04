import random
from time import localtime
from requests import get, post
from datetime import datetime, date
import sys
import os
 
 
def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)
 
 
def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token
 
 
def get_weather(region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    key = config["weather_key"]
    region_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(region, key)
    response = get(region_url, headers=headers).json()
    if response["code"] == "404":
        print("推送消息失败，请检查地区名是否有误！")
        os.system("pause")
        sys.exit(1)
    elif response["code"] == "401":
        print("推送消息失败，请检查和风天气key是否正确！")
        os.system("pause")
        sys.exit(1)
    else:
        # 获取地区的location--id
        location_id = response["location"][0]["id"]
    # 天气信息
    weather_url = "https://devapi.qweather.com/v7/weather/3d?location={}&key={}".format(location_id, key)
    response = get(weather_url, headers=headers).json()
    # 穿衣建议
    dress_url = "https://devapi.qweather.com/v7/indices/1d?type=3&location={}&key={}".format(location_id, key)
    response_dress = get(dress_url, headers=headers).json()
    # 白天天气
    textDay = response["daily"][0]["textDay"]
    # 夜间天气
    textNight = response["daily"][0]["textNight"]
    # 温度
    temp = response["daily"][0]["tempMin"] + u"\N{DEGREE SIGN}" + "C ~ " + response["daily"][0]["tempMax"] + u"\N{DEGREE SIGN}" + "C"
    # 穿衣建议
    dress = response_dress["daily"][0]["text"]
    return textDay, textNight, temp, dress


def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 获取国历生日的今年对应月和日
    birthday_month = int(birthday.split("-")[1])
    birthday_day = int(birthday.split("-")[2])
    # 今年生日
    year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day

# 获取天行数据
def get_tian():
    key = config["tian_key"]
    # 星座运势
    ConstellationChart = get_ConstellationChart(key)
    return ConstellationChart


# 星座运势
def get_ConstellationChart(key):
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    # 星座
    constellation = config["constellation"]

    region_url = "http://api.tianapi.com/star/index?key={}&astro={}&date={}".format(key, constellation, today)
    response = get(region_url).json()
    if response["code"] != 200:
        print("星座运势数据获取错误")
        os.system("pause")
        sys.exit(1)
    else:
        data = response["newslist"]
    return data

 
def send_message(to_user, access_token, region_name, textDay, textNight, temp, dress, ChickenSoup, ConstellationChart):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 问候语
    greetings = config["greetings"]
    # 星座
    constellation = config["constellation"]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            # 问候语
            "greetings": {
                "value": greetings,
                "color": get_color()
            },
            # 当前日期
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            # 城市
            "region": {
                "value": region_name,
                "color": get_color()
            },
            # 白天天气
            "textDay": {
                "value": textDay,
                "color": get_color()
            },
            # 夜间天气
            "textNight": {
                "value": textNight,
                "color": get_color()
            },
            # 气温
            "temp": {
                "value": temp,
                "color": get_color()
            },
            # 穿衣建议
            "FashionAdvice": {
                "value": dress,
                "color": get_color()
            },
            # 恋爱时间
            "love_day": {
                "value": love_days,
                "color": get_color()
            },
            # 星座
            "constellation": {
                "value": constellation,
                "color": get_color()
            },
            # 综合指数
            "omprehensiveIndex": {
                "value": ConstellationChart[0]["content"],
                "color": get_color()
            },
            # 爱情指数
            "loveIndex": {
                "value": ConstellationChart[1]["content"],
                "color": get_color()
            },
            # 工作指数
            "workIndex": {
                "value": ConstellationChart[2]["content"],
                "color": get_color()
            },
            # 财运指数
            "fortuneIndex": {
                "value": ConstellationChart[3]["content"],
                "color": get_color()
            },
            # 健康指数
            "healthIndex": {
                "value": ConstellationChart[4]["content"],
                "color": get_color()
            },
            # 幸运颜色
            "LuckyColor": {
                "value": ConstellationChart[5]["content"],
                "color": get_color()
            },
            # 幸运数字
            "LuckyNumbers": {
                "value": ConstellationChart[6]["content"],
                "color": get_color()
            },
            # 贵人星座
            "NobleConstellation": {
                "value": ConstellationChart[7]["content"],
                "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value["birthday"], year, today)
        if birth_day == 0:
            birthday_data = "今天{}生日哦，祝{}生日快乐！".format(value["name"], value["name"])
        else:
            birthday_data = "距离{}的生日还有{}天".format(value["name"], birth_day)
        # 将生日数据插入data
        data["data"][key] = {"value": birthday_data, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)
 
 
if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)
 
    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入地区获取天气信息
    region = config["region"]
    textDay, textNight, temp, dress = get_weather(region)
    # 天行数据
    ConstellationChart = get_tian()
    # 公众号推送消息
    for user in users:
        send_message(user, accessToken, region, textDay, textNight, temp, dress, ConstellationChart)
    os.system("pause")
