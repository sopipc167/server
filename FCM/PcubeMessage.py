from firebase_admin.messaging import Message,Notification
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler(daemon = True)
class Pcube_plus_msg():
    def __init__(self,title,content,token):
        self.title = title
        self.msg = content
        self.regis = token
        self.is_multi = False
    @classmethod
    def set_topic(cls,title,content,topic):
        return cls(title,content,topic)
        cls.is_multi=True
    @sched.scheduled_job('cron', minuite = '5', id  = "프로세스")
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