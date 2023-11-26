from apscheduler.schedulers.background import BackgroundScheduler

class Singleton(type):
    instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]

class PCubeScheduler(metaclass=Singleton):
    sched = BackgroundScheduler(daemon =True)
    sched.start()

    @classmethod
    def add_schedule_cron(cls, func ,**kwargs): # 시간 예약 메소드
        cls.sched.add_job(func, "cron", hour = kwargs['hour'], minute = kwargs['minute'], id = kwargs['id'],
                          start_date = kwargs['start_date'], end_date = kwargs['end_date'],args=[kwargs['args']])

    @classmethod
    def cancel_schedule_cron(cls,id):
        cls.sched.remove_job(job_id=id)