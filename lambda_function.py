import os
import requests
import json

# 1. APIから遅延情報を取得
def fetch_tommorow_weather_info():
    api_url ='https://api.open-meteo.com/v1/forecast?latitude=35.5533&longitude=139.6408&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FTokyo&forecast_days=1'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
# 2. メッセージの整形
def format_message(message):
    new_message = message['daily']
    weather =  {0:"晴れ", 1:"晴れ",2:"曇り",3:"曇り",51:"小雨",53:"雨",55:"大雨",61:"小雨",63:"雨",65:"大雨"}
    weather_code = new_message['weather_code'][0]
    temperature_max = new_message['temperature_2m_max'][0]
    temperature_min = new_message['temperature_2m_min'][0]
    forcast_weather = "自分で検索してください"
    if weather_code in weather.keys():
        forcast_weather = weather[weather_code]
    return forcast_weather,temperature_max,temperature_min

#3. Line MessagingAPIで通知
def send_line_notify(message):
    line_notify_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
    to = os.environ['LINE_CHANNEL_ID']
    headers = {
        'Authorization': f'Bearer {line_notify_token}'
    }
    data = {
        'to':to,
        'messages': message
    }
    requests.post('https://api.line.me/v2/bot/message/push', headers=headers, data=json.dumps(data))

# メイン処理
# def main():
def lambda_handler(event, context):
    data = fetch_tommorow_weather_info()
    if data:
        forcast_weather,temperature_max,temperature_min = format_message(data)
        notify_messge = f"明日の天気は{forcast_weather}です。\n最高気温は{temperature_max}度、最低気温は{temperature_min}度です。"
        send_line_notify(notify_messge)
    else:
        send_line_notify("天気情報の取得に失敗しました")
