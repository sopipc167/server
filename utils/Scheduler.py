from apscheduler.schedulers.background import BackgroundScheduler

class Singleton(type):
    instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]
class PCubeScheduler(metaclass=Singleton):
    sched = BackgroundScheduler