from firebase_admin.messaging import Message,Notification
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler(daemon = True)
class PcubePlusMsg():

    def __init__(self,title,content,token,dow,h,m):
        self.title = title
        self.msg = content
        self.regis = token
        self.hour = h
        self.minute = m
        self.day_of_week = dow
        self.is_multi = False

    @classmethod
    def set_topic(cls,title,content,topic):
        cls.is_multi = True
        return cls(title,content,topic)
    def set_schedule(self):
        sched.scheduled_job('cron', hour=self.hour, minute=self.minute, id='test_2')
    @set_schedule
    async def send_msg(self):
        if self.is_multi:
            msg = Message(
                notification=Notification(
                    title=self.title,
                    body=self.msg
                ),
                topic = self.regis
            )
        else:
            msg = Message(
                notification=Notification(
                    title=self.title,
                    body=self.msg
                ),
                token=self.regis
            )