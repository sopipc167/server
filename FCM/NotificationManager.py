import schedule
from database.database import Database
from FCM.FCMNotification import fcmNotification
import firebase_admin
import asyncio
from firebase_admin import credentials,messaging

cred = credentials.Certificate("violet-strike-firebase-adminsdk-2dlvt-8b8e680cb3.json")
firebase_admin.initialize_app(cred)

FCM_LIST =[]
def fetch_data(): #데이터베이스에서 알림 정보를 가져와서 알림 객체를 생성함
    database=Database()
    sql =f'select n.* from notification as n;'
    lst=database.execute_all(sql)
    database.close()
    for i in lst:
        tmp=fcmNotification(i,'f0I4IU3XRuiWCsSEyuyubQ:APA91bEiQFBUtlAhLheP0hfvSnEsAgsLSUlIVAJADz-TgPDfqj9TW4-TzmMfnoBicUpyyB-QHLcExke7nrWHcfIo-7bCFfDCGybY9IulXFUV-Plbz8CH2gwR5gFTFf2Fm1m5ifplb4fn')
        tmp.startSchedule()
        FCM_LIST.append(tmp)
    print(FCM_LIST)
def delete_notification(n):
    FCM_LIST.remove(n)
def register_topic(topic, registration_tokens): #FCM 토픽을 구독함
    response = messaging.subscribe_to_topic(registration_tokens, topic)
    print(response, '주제 구독을 성공적으로 완료함')

def unregister_topic(topic, registration_tokens):
    response = messaging.unsubscribe_from_topic(registration_tokens, topic)
    print(response,'주제 구독해제를 성공적으로 완료함')

schedule.every().hour.do(fetch_data)
fetch_data()
while True:
    schedule.run_pending()