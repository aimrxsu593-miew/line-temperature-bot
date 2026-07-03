import requests
import os
from datetime import date

THAI_DAYS = ["จันทร์","อังคาร","พุธ","พฤหัสบดี","ศุกร์","เสาร์","อาทิตย์"]
THAI_MONTHS = ["","ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย.",
               "ก.ค.","ส.ค.","ก.ย.","ต.ค.","พ.ย.","ธ.ค."]

FRIDGE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfNConfgLPmmZz154ahT8Fwe-FUZgIXBHRoTMOEadnvUmTa_Q/viewform"
TOILET_URL = "https://docs.google.com/forms/d/e/1FAIpQLSes0amcEGbXa5mD1Bg09Z9OVMX9jW4_EbG5QUqksAP3hck3yQ/viewform"

def get_thai_date():
    today = date.today()
    day_name = THAI_DAYS[today.weekday()]
    month_name = THAI_MONTHS[today.month]
    year = today.year + 543
    return f"วัน{day_name}ที่ {today.day} {month_name} {year}"

def flex_message(thai_date):
    return {
        "type": "flex",
        "altText": "แจ้งเตือนบันทึก 5ส. ประจำสัปดาห์",
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
                        "contents": [{"type": "text", "text": "💧 5ส. ประจำสัปดาห์", "color": "#AED6F1", "size": "xs", "flex": 1}]
                    },
                    {"type": "text", "text": "แจ้งเตือนบันทึก 5ส. ประจำวัน", "color": "#D6EAF8", "size": "md", "weight": "bold", "margin": "sm"},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "sm",
                        "contents": [
                            {"type": "text", "text": f"📅 {thai_date}", "color": "#AED6F1", "size": "xs", "flex": 3},
                            {"type": "text", "text": "⏰ 08:00 น.", "color": "#AED6F1", "size": "xs", "flex": 2, "align": "end"}
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
                            {"type": "text", "text": "🌡️ บันทึกอุณหภูมิตู้เย็น", "size": "sm", "weight": "bold", "color": "#154360"},
                            {"type": "text", "text": "กรุณาบันทึกอุณหภูมิและลงลายมือชื่อให้ครบถ้วน", "size": "xs", "color": "#555555", "wrap": True, "margin": "sm"},
                            {"type": "button", "action": {"type": "uri", "label": "บันทึกอุณหภูมิตู้เย็น", "uri": FRIDGE_URL}, "style": "primary", "color": "#154360", "margin": "sm", "height": "sm"}
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
                            {"type": "text", "text": "🚿 บันทึกการทำความสะอาดห้องน้ำ", "size": "sm", "weight": "bold", "color": "#0E6655"},
                            {"type": "text", "text": "กรุณาบันทึกการทำความสะอาดและลงลายมือชื่อให้ครบถ้วน", "size": "xs", "color": "#555555", "wrap": True, "margin": "sm"},
                            {"type": "button", "action": {"type": "uri", "label": "บันทึกการทำความสะอาด", "uri": TOILET_URL}, "style": "primary", "color": "#0E6655", "margin": "sm", "height": "sm"}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#EBF5FB",
                "paddingAll": "8px",
                "contents": [{"type": "text", "text": "📌 โปรดดำเนินการภายในเวลาที่กำหนด", "size": "xs", "color": "#154360", "align": "center"}]
            }
        }
    }

def send_flex(token, group_id, messages):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"to": group_id, "messages": messages}
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    TOKEN = os.environ["LINE_TOKEN"]
    GROUP_ID = os.environ["LINE_GROUP_ID"]
    thai_date = get_thai_date()
    send_flex(TOKEN, GROUP_ID, [flex_message(thai_date)])
