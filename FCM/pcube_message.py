class PcubePlusMsg():
    number=0
    def __new__(cls, *args, **kwargs):
        cls.is_multi = False
    def __init__(self, title, content, token, dow, h, end_date):
        global number
        number+=1
        self.title = title
        self.msg = content
        self.regis = token
        self.hour = h
        self.day_of_week = dow
        self.end_date = end_date
        self.id = f"msg{number}"

    @classmethod
    def set_topic(cls, title, content, topic):
        cls.is_multi = True
        return cls(title,content,topic)

    @classmethod
    def discard_topic(cls, title, content, topic):
        cls.is_multi = False
        return cls(title,content)