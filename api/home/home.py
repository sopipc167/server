from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from datetime import datetime, date

home = Namespace('home')

@home.route('/attendance')
class HomeAttendanceAPI(Resource):
    def get(self):
        current_date = datetime.today()

        database = Database()

        sql = f"SELECT * FROM schedules "\
            f"WHERE title = '판도라큐브 정기회의' AND start_date >= '{current_date}' "\
            f"ORDER BY start_date LIMIT 1;"
        
        next_meeting = database.execute_one(sql)

        if next_meeting is None:
            return { 'message': '예정된 회의가 없습니다. :(' }, 200
        else:
            next_meeting['start_date'] = next_meeting['start_date'].strftime('%Y-%m-%d')
            next_meeting['start_time'] = (datetime.min + next_meeting['start_time']).strftime('%H:%M')

            return next_meeting, 200

@home.route('/schedule')
class HomeScheduleAPI(Resource):
    def get(self):
        database = Database()


        sql = f"SELECT * FROM schedules ORDER BY start_date;"

        schedule_list = database.execute_all(sql)

        if not schedule_list:
            return {}, 200
        else:
            for idx, schedule in enumerate(schedule_list):
                # date 및 category를 문자열로 변환
                schedule_list[idx]['start_date'] = schedule['start_date'].strftime('%Y-%m-%d')
                if schedule['end_date']:
                    schedule_list[idx]['end_date'] = schedule['end_date'].strftime('%Y-%m-%d')
                if schedule['start_time']:
                    schedule_list[idx]['start_time'] = (datetime.min + schedule['start_time']).strftime('%H:%M')

        return schedule_list

@home.route('/product')
class HomeProductAPI(Resource):
    def get(self):
        pass