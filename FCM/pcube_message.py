from firebase_admin.messaging import Message,Notification
class PcubePlusMsg(Notification):
    number=0
    def __init__(self, token, reserved, is_multi, **kwargs):
        PcubePlusMsg.number += 1
        self.title = kwargs['title']
        self.msg = kwargs['content']
        self.id = f"msg{PcubePlusMsg.number}"
        self.token = token

        if reserved:
            self.hour = kwargs['hour']
            self.minute = kwargs['minute']
            self.day_of_week = kwargs['day_of_week']
            self.start_date = kwargs['start_date']
            self.end_date = kwargs['end_date']

        if is_multi:
            self.topic = kwargs['topic']
        else:
            self.is_multi = False

    def set_topic(self, title, content, topic):
        self.is_multi = True
        self.topic = topic

    def discard_topic(self, title, content, topic):
        self.is_multi = False