# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
from __future__ import print_function

import datetime as DateTime
from datetime import datetime, timedelta
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# 파일로 가져오는거로 바꾸면 될 것 같습니다~
CID = 'pcube.team@gmail.com'

class PCubeCalendar:
    def __init__(self, service):
        self.__service = service
    
    def get_monthly_events(self, year = None, month = None):
        if year == None: year = datetime.now().year
        if month == None: month = datetime.now().month

        events = self.__get_events_from_record(year, month)
        if events: return events
        print("update %d-%d" % (year, month))

        min_date = DateTime.date(year, month, 1)
        if month == 12: max_date = DateTime.date(year + 1, 1, 1) - timedelta(days = 1)
        else: max_date = DateTime.date(year, month + 1, 1) - timedelta(days = 1)

        min_date = min_date.isoformat() + 'T00:00:00Z'
        max_date = max_date.isoformat() + 'T00:00:00Z'

        results = self.__get_events_from_api(min_date, max_date)
        for result in results:
            events.append(self.__json_to_event(result))
        
        self.__record_event(year, month, events)

        return events

    # 굳이 이렇게 함수 뺄 필요 없긴 한데..그냥 해봣씁니다
    def __json_to_event(self, json_data):
        event = {}
        event['name'] = json_data.get('summary', 'Unknown')
        event['start_date'] = json_data['start'].get('dateTime', None)
        if event['start_date'] == None:
            event['has_span'] = True

            event['start_date'] = json_data['start'].get('date')
            event['end_date'] = json_data['end'].get('date')
        else: event['end_date'] = json_data['end'].get('dateTime')

        return event

    def __get_events_from_record(self, year, month):
        json_data = self.__get_record_json()
            
        target_events = json_data.get("%d-%d" % (year, month), None)
        if not target_events: return []
        
        last_update = datetime.strptime(target_events['last_update'], '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - last_update).seconds > 300: return []
  
        return target_events['events']
    
    def __record_event(self, year, month, events):
        json_data = self.__get_record_json()
        json_data[("%d-%d" % (year, month))] = {
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'events': events
        }

        with open('records.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file)
    
    def __get_record_json(self):
        path = 'records.json'

        json_data = {}
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8'):
                pass
        try:
            file = open(path, 'r', encoding='utf-8')
            json_data = json.load(file)

            file.close()
        except json.decoder.JSONDecodeError:
            pass

        return json_data

    def __get_events_from_api(self, timeMin = None, timeMax = None, maxResults = None):
        try:
            events_result = self.__service.events().list(
                calendarId = 'pcube.team@gmail.com', 
                timeMin = timeMin,
                timeMax = timeMax,
                maxResults = maxResults,
                singleEvents = True,
                orderBy = 'startTime').execute()

            events = events_result.get('items', [])
            if not events: return []
            return events
        except HttpError as error:
            print('An error occurred: %s' % error)
            return None


def get_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
    except HttpError as error:
        print('An error occurred: %s' % error)
        service = None
    
    return PCubeCalendar(service)