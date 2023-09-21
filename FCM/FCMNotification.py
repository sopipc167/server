from firebase_admin import messaging
from firebase_admin.messaging import Message,Notification
import schedule
import datetime
import asyncio

class fcmNotification(): #알림 객체
    DAY_OF_WEEK ={0:'monday', 1:'tuesday',2:'wendsday',3:'thursday',4:'frieday',5:'saturday',6:'sunday'} #알림의 요일을 영어로 바꾸기 위한 딕셔너리
    scheduler = ""
    expire_day = datetime.datetime
    start_day = datetime.datetime
    week = ''
    time = datetime.timedelta
    cycle = ''
    def __init__(self, data, token): #API Key와 앱 토큰을 초기화
        self.DATA = data
        self.TOKEN = token
        self.setSchedule(data)
    def __del__(self):
        print(f'{self.DAY_OF_WEEK[self.week]} {self.time}시에 예약된 알람을 삭제했습니다.')
    def check_expired(self):
        if datetime.datetime.now() <= self.expire_day:
            return True
        else:
            return False
    async def sendMessage(self,body, title):
        if self.check_expired():#만약 날짜가 만료되면 자동으로 스케쥴 취소
            self.__del__()
            return schedule.CancelJob
        # 메시지 (data 타입)
        message = Message(
            notification=Notification(
                title=title,
                body=body
            ),
            token=self.TOKEN
        )
        result = messaging.send(message)# 토큰값을 이용해 1명에게 푸시알림을 전송함
        return await result
    async def sendtopicMessage(self,body, title,topic):
        if self.check_expired():#만약 날짜가 만료되면 자동으로 스케쥴 취소
            self.__del__()
            return schedule.CancelJob
        # 메시지 (data 타입)
        message = Message(
            notification=Notification(
                title=title,
                body=body
            ),
            topic=topic
        )
        result = messaging.send_each_for_multicast(message) #여러명에게 topic을 이용해 메세지 전송
        return await result
    async def runcoroutine(self,m,n):
        aws = self.sendMessage(m,n)
        await asyncio.gather(*aws)
        print(aws)
    def startSchedule(self): #스케쥴을 시작함
        exec(f'asyncio.run({self.scheduler})')
    def timeparser(self):
        pass
    def setSchedule(self, data): #스케쥴을 설정하여 몇일, 몇주 주기로 메세지를 보낼지 결정\
        self.time=data['time']
        self.week=data['day']
        self.start_date=data['start_date']
        self.expire_day=data['end_date']
        self.cycle = data['cycle']
        message=data['message']
        memo=data['memo']
        self.scheduler=  f"schedule.every(5).seconds.do(self.sendMessage,\"{message}\",\"{memo}\")"
        pass
        """
        if(self.cycle=='매주'):
            self.scheduler = f"schedule.every().{self.DAY_OF_WEEK[self.week]}.at(\"{self.time}\").do(self.runcoroutine,\"{message}\",\"{memo}\")"
        elif(self.cycle=='매일'):
            self.scheduler = f"schedule.every().day.at(\"{time}\").do(self.sendMessage,{message},{memo})"
        else:
            self.scheduler = None
        """
    def test(self):
        print('hello')
