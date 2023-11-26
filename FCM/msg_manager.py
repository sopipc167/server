import firebase_admin
from firebase_admin import credentials,messaging
from pcube_message import PcubePlusMsg
import configparser
from utils.Scheduler import PCubeScheduler, Singleton
from firebase_admin.messaging import Message,Notification

config = configparser.ConfigParser()
config.read_file(open('../config/config.ini'))

class NotificationManager(metaclass=Singleton):
    cred_path = config['NOTIFICATION']['CRED_PATH']
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

    def __init__(self):
        self.msg_lst=[]

    def register_message(self, token, is_multi, reserved, **data):
        instance = PcubePlusMsg(token=token, reserved = reserved, is_multi=is_multi, **data)
        self.msg_lst.append(instance)
        if reserved:
            PCubeScheduler.add_schedule_cron(self.send_msg, args = instance ,day_of_week = instance.day_of_week, hour = instance.hour, minute = instance.minute, start_date = instance.start_date,
                                        end_date=instance.end_date, id = instance.id)
        else:
            self.send_msg(instance)

    def register_topic(self, topic, registration_tokens):  # FCM 토픽을 구독함
        response = messaging.subscribe_to_topic(registration_tokens, topic)
        print(response, '주제 구독을 성공적으로 완료함')

    def unregister_topic(self, topic, registration_tokens): # FCM 토픽을 구독 해제함
        response = messaging.unsubscribe_from_topic(registration_tokens, topic)
        print(response, '주제 구독해제를 성공적으로 완료함')

    def delete_msg(self, id):
        for i in self.msg_lst:
            if i.id == id:
                print(i)
                PCubeScheduler.cancel_schedule_cron(id=id)
                self.msg_lst.remove(i)
                del i

    def send_msg(self, msg): # 메세지 전송 메소드
        if msg.is_multi:
            msg = Message(
                notification=Notification(
                    title=msg.title,
                    body=msg.content
                ),
                topic = msg.topic
            )
        else:
            msg = Message(
                notification=Notification(
                    title=msg.title,
                    body=msg.msg
                ),
                token=msg.token
            )
        response = messaging.send(msg)
        print(response)

tst = NotificationManager()
t='dyCOhH_fTpKno1yAueHHvD:APA91bGNjHHBPesdd35gm30HzAArIc-3BgSQPENQ5ZNGLzilTODRGarNz9Zks29oor4PlrEgbnCW0R_76FLtY2eOdvdD07WS5MB1c7wLeHAr8SEoTcNfsLeINp_OBFWb73raEJCt8iFH'
dat = {'title': '테스트', 'content': '예약 메세지2s', 'day_of_week': 'sun', 'hour': 19, 'minute': 7,
       'start_date': '2023-11-20', 'end_date': '2023-11-30'}
