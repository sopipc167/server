import firebase_admin
from firebase_admin import credentials,messaging
from pcube_message import PcubePlusMsg
import configparser
from utils.Scheduler import PCubeScheduler
from firebase_admin.messaging import Message,Notification

config = configparser.ConfigParser()
config.read_file(open('config/config.ini'))

class NotificationManager:
    cred_path =  config['NOTIFICATION']['CRED_PATH']
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    def __init__(self):
        self.msg_lst=[]
    def register_message(self,data,token):
        title = data['message']
        content = data['memo']
        day_of_week=data['cycle']
        cron = data['time']
        token = ""
        self.msg_lst.append(PcubePlusMsg(title,content,token,day_of_week,cron))
    def delete_notification(n):
        pass

    def register_topic(topic, registration_tokens):  # FCM 토픽을 구독함
        response = messaging.subscribe_to_topic(registration_tokens, topic)
        print(response, '주제 구독을 성공적으로 완료함')

    def unregister_topic(topic, registration_tokens):
        response = messaging.unsubscribe_from_topic(registration_tokens, topic)
        print(response, '주제 구독해제를 성공적으로 완료함')

    def cancel_schedule(self):
        PCubeScheduler.sched.remove_job(id = self.id)

    async def send_msg(self, msg):
        if msg.is_multi:
            msg = Message(
                notification=Notification(
                    title=msg.title,
                    body=msg.content
                ),
                topic = msg.regis
            )
        else:
            msg = Message(
                notification=Notification(
                    title=msg.title,
                    body=msg.msg
                ),
                token=msg.regis
            )
        PCubeScheduler.add_schedule_cron(day_of_week=msg.dow, h=msg.hour, m=msg.minute, start_date=msg.end_date,
                                         id=msg.id)
