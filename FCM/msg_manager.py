import firebase_admin
from firebase_admin import credentials,messaging
from PcubeMessage import Pcube_plus_msg
class Notification_manager:
    cred_path = "violet-strike-firebase-adminsdk-2dlvt-8b8e680cb3.json"
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    def __init__(self):
        self.msg_lst=[]
    def register_message(self,data,token):
        title = data['message']
        content = data['memo']
        token = ""
        self.msg_lst.append(Pcube_plus_msg(title,content,token))
    def delete_notification(n):
        pass

    def register_topic(topic, registration_tokens):  # FCM 토픽을 구독함
        response = messaging.subscribe_to_topic(registration_tokens, topic)
        print(response, '주제 구독을 성공적으로 완료함')

    def unregister_topic(topic, registration_tokens):
        response = messaging.unsubscribe_from_topic(registration_tokens, topic)
        print(response, '주제 구독해제를 성공적으로 완료함')