from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
# 从环境变量中获取配置信息
start_date = os.environ.get('START_DATE', '')
city = os.environ.get('CITY', '')
birthday = os.environ.get('BIRTHDAY', '')
app_id = os.environ.get("APP_ID", '')
app_secret = os.environ.get("APP_SECRET", '')
user_id = os.environ.get("USER_ID", '')
template_id = os.environ.get("TEMPLATE_ID", '')
# 微信公众号配置
client = WeChatClient(appid=app_id, secret=app_secret)
wm = WeChatMessage(client)
def get_weather():
    url = f"http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city={city}"
    try:
        res = requests.get(url).json()
        weather = res['data']['list'][0]
        return weather['weather'], math.floor(weather['temp'])
    except Exception as e:
        print(f"获取天气失败: {str(e)}")
        return None, None
def get_count():
    try:
        today = datetime.now()
        delta = today - datetime.strptime(start_date, "%Y-%m-%d")
        return delta.days
    except Exception as e:
        print(f"获取天数失败: {str(e)}")
        return None
def get_birthday():
    try:
        today = datetime.now()
        next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
        if next < today:
            next = next.replace(year=next.year + 1)
        return (next - today).days
    except Exception as e:
        print(f"获取生日天数失败: {str(e)}")
        return None
def get_words():
    try:
        words = requests.get("https://api.shadiao.pro/chp")
        if words.status_code == 200:
            return words.json().get('data', {}).get('text', '')
        else:
            print(f"请求文字失败: {words.status_code}")
    except Exception as e:
        print(f"获取文字失败: {str(e)}")
    return ''
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)
# 获取相关数据
wea, temperature = get_weather()
count = get_count()
birthday_left = get_birthday()
words = get_words()
if wea is not None and temperature is not None and count is not None and birthday_left is not None:
    # 构建模板消息数据
    data = {
        "weather": {"value": wea},
        "temperature": {"value": temperature},
        "love_days": {"value": count},
        "birthday_left": {"value": birthday_left},
        "words": {"value": words, "color": get_random_color()}
    }
    # 发送模板消息
    try:
        res = wm.send_template(user_id, template_id, data)
        print(res)
    except Exception as e:
        print(f"发送模板消息失败: {str(e)}")
else:
    print("获取数据失败")
