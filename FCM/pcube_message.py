from firebase_admin.messaging import Message,Notification
from utils.Scheduler import PCubeScheduler
class PcubePlusMsg():
    number=0
    def __init__(self,title,content,token,dow,h,end_date):
        global number
        number+=1
        self.title = title
        self.msg = content
        self.regis = token
        self.hour = h
        self.day_of_week = dow
        self.is_multi = False
        self.end_date =end_date
        self.id = f"msg{number}"
        PCubeScheduler.add_schedule_cron(day_of_week = dow,h=self.hour,m=self.minute,start_date =self.end_date,id=self.id)

    def cancel_schedule(self):
        PCubeScheduler.sched.remove_job(id = self.id)

    @cancel_schedule()
    def __del__(self):
        pass

    @classmethod
    def set_topic(cls,title,content,topic):
        cls.is_multi = True
        return cls(title,content,topic)

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