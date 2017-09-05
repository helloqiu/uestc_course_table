# -*- coding: utf-8 -*-

import argparse
import json
import os
import httplib2
import datetime
import socket
import socks

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

DESCRIPTION = """把课程表导入到 Google Calendar。"""
SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_SECRET_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'secret.json')
APPLICATION_NAME = "uestc course table"
CLASS_LENGTH = {
    '2': 95,
    '3': 145,
    '4': 205
}
CLASS_START = {
    '1': 510,
    '3': 620,
    '5': 870,
    '7': 980,
    '9': 1170
}

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('-c', type=str, help="课程 json 文件的位置", metavar="position")
parser.add_argument('-d', type=str, help="开学第一周的周一的年月日，例如 2017-09-01", metavar="date")
parser.add_argument('-p', type=str, help="google 当然不能国内访问啦，你需要一个 socks5 代理，例如 localhost:1080",
                    metavar="address:port")


def get_credentials():
    credential_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'calendar.json')
    if not os.path.exists(credential_path):
        from pathlib import Path
        Path(credential_path).touch()

    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    args = parser.parse_args()
    if not args.c:
        raise RuntimeError('你得告诉我课程json文件的位置')
    if not args.d:
        raise RuntimeError('你得告诉我开学的日期')
    if not args.p:
        raise RuntimeError('你得告诉我你的代理')
    address = args.p[:args.p.find(':')]
    port = int(args.p[args.p.find(':') + 1:])

    socks.set_default_proxy(socks.SOCKS5, address, port)
    socket.socket = socks.socksocket

    with open(args.c, 'r') as f:
        course_data = json.loads(f.read())

    d = datetime.datetime.strptime(args.d, '%Y-%m-%d')

    events = []
    for course in course_data:
        start = datetime.datetime(
            year=d.year,
            month=d.month,
            day=d.day
        )
        start = start + datetime.timedelta(days=course['weekday'] - 1, minutes=CLASS_START[str(course['start_time'])])
        end = start + datetime.timedelta(minutes=CLASS_LENGTH[str(course['length'])])
        event = {
            'description': '教师:{}\n课程名称:{}\n教室:{}'.format(course['teacher'], course['name'], course['location']),
            'location': course['location'],
            'summary': course['name'],
            'start': {
                'dateTime': start.isoformat('T'),
                'timeZone': 'Asia/Shanghai'
            },
            'end': {
                'dateTime': end.isoformat('T'),
                'timeZone': 'Asia/Shanghai'
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;COUNT={}'.format(course['end_week'] - course['start_week'] + 1)
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 30}
                ]
            }
        }
        events.append(event)

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    for event in events:
        e = service.events().insert(calendarId='primary', body=event).execute()
        print('添加课程: {}\n\tURL: {}'.format(event['summary'], e.get('htmlLink')))
    print('添加成功')
