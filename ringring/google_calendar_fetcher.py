from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GoogleCalendarFetcher:
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def __init__(self, credentials_path=None, token_path=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.credentials_path = credentials_path or os.path.join(base_dir, "credentials.json")
        self.token_path = token_path or os.path.join(base_dir, "token.json")
        self.creds = None
        self.service = None

    def authenticate(self):
        """认证并初始化 Google Calendar API 服务"""
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        # 如果没有凭证或者凭证失效，重新认证
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # 保存凭证
            with open(self.token_path, 'w') as token_file:
                token_file.write(self.creds.to_json())

        self.service = build('calendar', 'v3', credentials=self.creds)

    def fetch_events(self, hours_before=12, hours_after=12):
        """获取当前时间前后hours_before和hours_after小时内的事件"""
        if not self.service:
            raise Exception("Google Calendar API service not initialized. Call authenticate() first.")

        now = datetime.datetime.utcnow()
        time_min = (now - datetime.timedelta(hours=hours_before)).isoformat() + 'Z'  # 'Z'表示UTC时间
        time_max = (now + datetime.timedelta(hours=hours_after)).isoformat() + 'Z'

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        results = []
        for event in events:
            attendees = event.get('attendees', [])
            keep = True
            for attendee in attendees:
                if attendee.get('self'):
                    status = attendee.get('responseStatus')
                    if status == 'declined':
                        keep = False
                        break
            if keep:
                event_info = {
                    'id': event.get('id'),
                    'summary': event.get('summary'),
                    'description': event.get('description', ''),
                    'start': event['start'].get('dateTime', event['start'].get('date')),
                    'end': event['end'].get('dateTime', event['end'].get('date')),
                    'hangoutLink': event.get('hangoutLink') or event.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri', '')
                }
                results.append(event_info)

        return results

if __name__ == '__main__':
    fetcher = GoogleCalendarFetcher()
    fetcher.authenticate()
    events = fetcher.fetch_events()
    for e in events:
        print(f"{e['start']} - {e['summary']} - {e['hangoutLink']}")