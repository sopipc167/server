import schedule
from database.database import Database
from FCM.FCMNotification import Notification
from pyfcm import FCMNotification
import firebase_admin
from firebase_admin import credentials,messaging

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

default_app = firebase_admin.initialize_app()

FCM_LIST =[]
def fetch_data(): #데이터베이스에서 알림 정보를 가져와서 알림 객체를 생성함
    database=Database()
    sql =f'select n.* from notification as n;'
    lst=database.execute_all(sql)
    database.close()
    for i in lst:
        tmp=Notification(i,'unknown string wanted','unknown string wanted')
        tmp.startSchedule()
        FCM_LIST.append(tmp)
def delete_notification(n):
    FCM_LIST.remove(n)
def register_topic(topic, registration_tokens): #FCM 토픽을 구독함
    response = messaging.subscribe_to_topic(registration_tokens, topic)
    print(response.success_count, 'tokens were subscribed successfully')

schedule.every().hour.do(fetch_data)

while True:
    schedule.run_pending()


