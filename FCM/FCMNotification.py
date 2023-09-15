from pyfcm import FCMNotification
from database.database import Database
import schedule
import datetime
import time

class Notification: #알림 객체
    DAY_OF_WEEK={'월요일':'monday','화요일':'tuesday','수요일':'wendsday','목요일':'thrsday','금요일':'frieday','토요일':'saturday','일요일':'sunday'} #알림의 요일을 영어로 바꾸기 위한 딕셔너리
    scheduler=""
    expire_day=datetime.datetime
    def __init__(self, data, apikey, token): #API Key와 앱 토큰을 초기화
        self.DATA = data
        APIKEY = apikey
        TOKEN = token
        push_service = FCMNotification(APIKEY)
        self.timeParser(data)

    def sendMessage(self,body, title):
        if datetime.datetime.now()<self.expire_day: #만약 날짜가 만료되면 자동으로 스케쥴 취소
            return schedule.CancelJob
        # 메시지 (data 타입)
        data_message = {
            "body": body,
            "title": title
        }
        result = self.push_service.single_device_data_message(registration_id=self.TOKEN, data_message=data_message)# 토큰값을 이용해 1명에게 푸시알림을 전송함
        print(result) # 전송 결과 출력
    def startSchedule(self): #스케쥴을 시작함
        eval(self.scheduler)
    def setSchedule(self, data): #스케쥴을 설정하여 몇일, 몇주 주기로 메세지를 보낼지 결정
        for i in data:
            time=i['time']
            week=i['day']
            start_date=i['start_date']
            self.expire_day=i['end_date']
            cycle = i['cyle']
            message=i['message']
            memo=i['memo']
        if(cycle=='매주'):
            self.scheduler = f"schedule.every().{self.DAY_OF_WEEK[week]}.at(\"{time}\").do(self.sendMessage,{message},{memo})"
        elif(cycle=='매일'):
            self.scheduler = f"schedule.every().day.at(\"{time}\").do(self.sendMessage,{message},{memo})"
        else:
            self.scheduler = None



    