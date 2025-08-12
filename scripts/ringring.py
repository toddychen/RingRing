import sys
import os
import datetime

# 添加项目根目录到 sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from ringring.google_calendar_fetcher import GoogleCalendarFetcher
from ringring.notification import Notification

REMIND_BEFORE_MINUTES = 100  # 提前/延后多少分钟提醒

def parse_iso_to_timestamp(time_str):
    if 'T' in time_str:
        dt = datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    else:
        dt = datetime.datetime.fromisoformat(time_str).replace(tzinfo=datetime.timezone.utc)
    return dt.timestamp()

def main():
    fetcher = GoogleCalendarFetcher()
    fetcher.authenticate()
    events = fetcher.fetch_events()

    now_ts = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).timestamp()

    for event in events:
        start_str = event.get('start')
        if not start_str:
            continue
        start_ts = parse_iso_to_timestamp(start_str)
        diff_min = abs((start_ts - now_ts) / 60)
        if diff_min <= REMIND_BEFORE_MINUTES:
            meeting_info = {
                "title": event.get("summary", "No Title"),
                "description": event.get("description", ""),
                "link": event.get("hangoutLink") or event.get("conferenceData", {}).get("entryPoints", [{}])[0].get("uri", "")
            }
            notification = Notification()
            notification.show(meeting_info)
            break

if __name__ == "__main__":
    main()