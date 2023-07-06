from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from datetime import datetime, date

accounting = Namespace('accounting')

# 회비 납부 상태 category (현재)
CURRENT_PAYMENT_STATE_CATEGORY = {1: '납부자', 2: '납부자', 4: '미납부자'}

# 회비 납부 상태 category (과거)
PAST_PAYMENT_STATE_CATEGORY = {1: '정상 납부', 2: '정상 납부', 3: '납부 지각', 4: '미납부자'}

# 유저 등급 category
USER_LEVEL_CATEGORY = {0: '정회원', 1: '수습회원'}

# index 데이터를 문자열로 변경
def convert_to_string(dictionary, index):
    return dictionary.get(index, None)
    

@accounting.route('/check')
class MembershipFeeCheckAPI(Resource):
    # 월별 회비 납부 내역 얻기
    def get(self):
        # 금월 및 작년 6월 날짜 구한 뒤 문자열로 변환 ('YYYY-MM-01' 형식)
        current_month = date(datetime.today().year, datetime.today().month, 1)
        start_month = date(current_month.year - 1, 6, 1)
        current_month.strftime('%Y-%m-%d')
        start_month.strftime('%Y-%m-%d')
        
        database = Database()

        # DB에서 월별 회비 납부 기간 불러오기
        sql = f"SELECT date, start_day, end_day FROM monthly_payment_periods "\
            f"WHERE date between '{start_month}' and '{current_month}' "\
            f"ORDER BY date;"
        
        payment_period_list = database.execute_all(sql)

        # DB에서 기간에 맞는 회비 납부 내역 불러오기
        sql = f"SELECT date, name, level, grade, amount, category FROM membership_fees mf "\
            f"JOIN users u ON mf.user_id = u.id "\
            f"WHERE date between '{start_month}' and '{current_month}' "\
            f"ORDER BY date;"
        
        user_payment_list = database.execute_all(sql)

        database.close()

        # 납부 기간 내역의 날짜 데이터들을 문자열로 변경
        for idx, payment_period in enumerate(payment_period_list):
            payment_period_list[idx]['date'] = payment_period['date'].strftime('%Y-%m-%d')
            payment_period_list[idx]['start_day'] = payment_period['start_day'].strftime('%Y-%m-%d')
            payment_period_list[idx]['end_day'] = payment_period['end_day'].strftime('%Y-%m-%d')

        # 회비 납부 내역의 날짜 및 index 데이터들을 문자열로 변경 
        for idx, user_payment in enumerate(user_payment_list):
            user_payment_list[idx]['date'] = user_payment['date'].strftime('%Y-%m-%d')

            if user_payment_list[idx]['date'] == current_month:
                user_payment_list[idx]['category'] = convert_to_string(CURRENT_PAYMENT_STATE_CATEGORY, user_payment['category'])
            else:
                user_payment_list[idx]['category'] = convert_to_string(PAST_PAYMENT_STATE_CATEGORY, user_payment['category'])

            user_payment_list[idx]['level'] = convert_to_string(USER_LEVEL_CATEGORY, user_payment['level'])

        # 월별 회비 납부 내역 만들기
        monthly_payment_list = []

        for payment_period in payment_period_list:
            monthly_payment = {}
            # 회비 납부 기간 추가
            monthly_payment.update(payment_period)

            # 회비 납부 내역 추가
            monthly_payment.update({'user_payment_list': []})

            for user_payment in user_payment_list:
                if user_payment['date'] == monthly_payment['date']:
                    monthly_payment['user_payment_list'].append(user_payment)

            monthly_payment_list.append(monthly_payment)


        if not monthly_payment_list: # 월별 회비 납부 내역이 없을 때의 처리
            return {}, 200
        else:
            return monthly_payment_list, 200
