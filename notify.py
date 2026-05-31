import requests
import json
from datetime import date

THAI_HOLIDAYS = {
    "2025-01-01", "2025-02-12", "2025-04-06", "2025-04-07",
    "2025-04-13", "2025-04-14", "2025-04-15", "2025-05-01",
    "2025-05-05", "2025-06-03", "2025-07-28", "2025-07-29",
    "2025-08-12", "2025-10-13", "2025-10-23", "2025-12-05",
    "2025-12-10", "2025-12-31",
    "2026-01-01", "2026-04-06", "2026-04-13", "2026-04-14",
    "2026-04-15", "2026-05-01", "2026-05-11", "2026-06-03",
    "2026-07-27", "2026-07-28", "2026-08-12", "2026-10-13",
    "2026-10-23", "2026-12-07", "2026-12-10", "2026-12-31",
}

def is_holiday_or_weekend():
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    weekday = today.weekday()
    return weekday >= 5 or today_str in THAI_HOLIDAYS

def send_line_message(token, group_id, message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": group_id,
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    import os
    import sys

    TOKEN = os.environ["LINE_TOKEN"]
    GROUP_ID = os.environ["LINE_GROUP_ID"]
    SESSION = sys.argv[1] if len(sys.argv) > 1 else "morning"

    if not is_holiday_or_weekend():
        print("วันทำการปกติ ไม่ส่งแจ้งเตือน")
        sys.exit(0)

    today_str = date.today().strftime("%d/%m/%Y")

    if SESSION == "morning":
        msg = (
            f"🌅 แจ้งเตือนบันทึกอุณหภูมิ (รอบเช้า)\n"
            f"📅 วันที่: {today_str}\n"
            f"⏰ เวลา: 08:00 น.\n\n"
            f"กรุณาบันทึกอุณหภูมิและความชื้นให้ครบถ้วน\n"
            f"พร้อมลงลายมือชื่อผู้บันทึก ✅"
        )
    else:
        msg = (
            f"🌤️ แจ้งเตือนบันทึกอุณหภูมิ (รอบบ่าย)\n"
            f"📅 วันที่: {today_str}\n"
            f"⏰ เวลา: 14:00 น.\n\n"
            f"กรุณาบันทึกอุณหภูมิและความชื้นให้ครบถ้วน\n"
            f"พร้อมลงลายมือชื่อผู้บันทึก ✅"
        )

    send_line_message(TOKEN, GROUP_ID, msg)
