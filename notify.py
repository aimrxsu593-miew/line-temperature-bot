import requests
import os
import sys
from datetime import date

THAI_HOLIDAY_CALENDAR = "th.th#holiday@group.v.calendar.google.com"

THAI_DAYS = ["จันทร์","อังคาร","พุธ","พฤหัสบดี","ศุกร์","เสาร์","อาทิตย์"]
THAI_MONTHS = ["","ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย.",
               "ก.ค.","ส.ค.","ก.ย.","ต.ค.","พ.ย.","ธ.ค."]

FRIDGE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfNConfgLPmmZz154ahT8Fwe-FUZgIXBHRoTMOEadnvUmTa_Q/viewform"
TOILET_URL = "https://docs.google.com/forms/d/e/1FAIpQLSes0amcEGbXa5mD1Bg09Z9OVMX9jW4_EbG5QUqksAP3hck3yQ/viewform"

def get_thai_holidays(api_key, year):
    url = "https://www.googleapis.com/calendar/v3/calendars/{}/events".format(
        requests.utils.quote(THAI_HOLIDAY_CALENDAR, safe='')
    )
    params = {
        "key": api_key,
        "timeMin": f"{year}-01-01T00:00:00Z",
        "timeMax": f"{year}-12-31T23:59:59Z",
        "singleEvents": True,
        "orderBy": "startTime"
    }
    response = requests.get(url, params=params)
    holidays = set()
    if response.status_code == 200:
        for event in response.json().get("items", []):
            start = event.get("start", {}).get("date")
            if start:
                holidays.add(start)
        print(f"โหลดวันหยุด {len(holidays)} วัน จาก Google Calendar")
    else:
        print(f"Google Calendar API error: {response.status_code} - {response.text}")
    return holidays

def is_holiday_or_weekend(api_key):
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    if today.weekday() >= 5:
        return True
    holidays = get_thai_holidays(api_key, today.year)
    return today_str in holidays

def get_thai_date():
    today = date.today()
    day_name = THAI_DAYS[today.weekday()]
    month_name = THAI_MONTHS[today.month]
    year = today.year + 543
    return f"วัน{day_name}ที่ {today.day} {month_name} {year}"

def flex_morning(thai_date):
    return {
        "type": "flex",
        "altText": "แจ้งเตือนบันทึก 5ส. ประจำวัน (รอบเช้า)",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#154360",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "💧 5ส. ประจำวัน",
                                "color": "#AED6F1",
                                "size": "xs",
                                "flex": 1
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": "แจ้งเตือนบันทึก 5ส. ประจำวัน",
                        "color": "#D6EAF8",
                        "size": "md",
                        "weight": "bold",
                        "margin": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"📅 {thai_date}",
                                "color": "#AED6F1",
                                "size": "xs",
                                "flex": 3
                            },
                            {
                                "type": "text",
                                "text": "⏰ 08:00 น.",
                                "color": "#AED6F1",
                                "size": "xs",
                                "flex": 2,
                                "align": "end"
                            }
                        ]
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#EBF5FB",
                        "cornerRadius": "10px",
                        "paddingAll": "12px",
                        "borderWidth": "1px",
                        "borderColor": "#AED6F1",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🌡️ บันทึกอุณหภูมิตู้เย็น",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#154360"
                            },
                            {
                                "type": "text",
                                "text": "กรุณาบันทึกอุณหภูมิและลงลายมือชื่อให้ครบถ้วน",
                                "size": "xs",
                                "color": "#555555",
                                "wrap": True,
                                "margin": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "บันทึกอุณหภูมิตู้เย็น",
                                    "uri": FRIDGE_URL
                                },
                                "style": "primary",
                                "color": "#154360",
                                "margin": "sm",
                                "height": "sm"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#E8F6F3",
                        "cornerRadius": "10px",
                        "paddingAll": "12px",
                        "borderWidth": "1px",
                        "borderColor": "#A2D9CE",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🚿 บันทึกการทำความสะอาดห้องน้ำ",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#0E6655"
                            },
                            {
                                "type": "text",
                                "text": "กรุณาบันทึกการทำความสะอาดและลงลายมือชื่อให้ครบถ้วน",
                                "size": "xs",
                                "color": "#555555",
                                "wrap": True,
                                "margin": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "บันทึกการทำความสะอาด",
                                    "uri": TOILET_URL
                                },
                                "style": "primary",
                                "color": "#0E6655",
                                "margin": "sm",
                                "height": "sm"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#EBF5FB",
                "paddingAll": "8px",
                "contents": [
                    {
                        "type": "text",
                        "text": "📌 โปรดดำเนินการภายในเวลาที่กำหนด",
                        "size": "xs",
                        "color": "#154360",
                        "align": "center"
                    }
                ]
            }
        }
    }

def flex_afternoon(thai_date):
    return {
        "type": "flex",
        "altText": "แจ้งเตือนบันทึก 5ส. ประจำวัน (รอบบ่าย)",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#154360",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "💧 5ส. ประจำวัน",
                                "color": "#AED6F1",
                                "size": "xs",
                                "flex": 1
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": "แจ้งเตือนบันทึก 5ส. ประจำวัน",
                        "color": "#D6EAF8",
                        "size": "md",
                        "weight": "bold",
                        "margin": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"📅 {thai_date}",
                                "color": "#AED6F1",
                                "size": "xs",
                                "flex": 3
                            },
                            {
                                "type": "text",
                                "text": "⏰ 14:00 น.",
                                "color": "#AED6F1",
                                "size": "xs",
                                "flex": 2,
                                "align": "end"
                            }
                        ]
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#EBF5FB",
                        "cornerRadius": "10px",
                        "paddingAll": "12px",
                        "borderWidth": "1px",
                        "borderColor": "#AED6F1",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🌡️ บันทึกอุณหภูมิตู้เย็น",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#154360"
                            },
                            {
                                "type": "text",
                                "text": "กรุณาบันทึกอุณหภูมิและลงลายมือชื่อให้ครบถ้วน",
                                "size": "xs",
                                "color": "#555555",
                                "wrap": True,
                                "margin": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "บันทึกอุณหภูมิตู้เย็น",
                                    "uri": FRIDGE_URL
                                },
                                "style": "primary",
                                "color": "#154360",
                                "margin": "sm",
                                "height": "sm"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#EBF5FB",
                "paddingAll": "8px",
                "contents": [
                    {
                        "type": "text",
                        "text": "📌 โปรดดำเนินการภายในเวลาที่กำหนด",
                        "size": "xs",
                        "color": "#154360",
                        "align": "center"
                    }
                ]
            }
        }
    }

def send_flex(token, group_id, messages):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"to": group_id, "messages": messages}
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    TOKEN = os.environ["LINE_TOKEN"]
    GROUP_ID = os.environ["LINE_GROUP_ID"]
    GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
    SESSION = sys.argv[1] if len(sys.argv) > 1 else "morning"

    if not is_holiday_or_weekend(GOOGLE_API_KEY):
        print("วันทำการปกติ ไม่ส่งแจ้งเตือน")
        sys.exit(0)

    thai_date = get_thai_date()

    if SESSION == "morning":
        messages = [flex_morning(thai_date)]
    else:
        messages = [flex_afternoon(thai_date)]

    send_flex(TOKEN, GROUP_ID, messages)
