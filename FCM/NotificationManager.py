import schedule
from database.database import Database
from FCM.FCMNotification import Notification

FCM_LIST =[]

def fetch_data(): #데이터베이스에서 알림 정보를 가져와서 알림 객체를 생성함
    database=Database()
    lst = []
    sql =f'select n.* from notification as n;'
    lst=database.execute_all(sql)
    database.close()
    for i in lst:
        tmp=Notification(i,'unknown string wanted','unknown string wanted')
        FCM_LIST.append(tmp)

while True:
    schedule.run_pending()


