from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from datetime import datetime

accounting = Namespace('accounting')

# 납부 상태 반환
def get_payment_state(monthly_payment):
    if monthly_payment['payment_date']:
        if monthly_payment['payment_date'] <= monthly_payment['end_day']:
            return "납부 완료"
        else:
            return "납부 지연"
    else:
        current_date = datetime.now().date()
        if current_date < monthly_payment['start_day']:
            return "기간 외"
        else:
            return "미납"
        
# 회원 등급 및 활동 여부에 따른 회비 반환
def get_amount(user_info):
    if user_info['level'] == 0 and user_info['grade'] == 4: 
        return 3000
    else:
        return 5000

@accounting.route('/<int:user_id>')
class AccountingUserAPI(Resource):
    def get(self, user_id):
        database = Database()

        # DB에서 user_id값에 맞는 월별 회비 납부 내역 불러오기
        sql = f"SELECT mpp.date, start_day, end_day, mf.date as payment_date, amount "\
            f"FROM monthly_payment_periods mpp "\
            f"LEFT JOIN membership_fees mf "\
            f"ON mf.user_id = {user_id} AND YEAR(mpp.date) = YEAR(mf.date) and MONTH(mpp.date) = MONTH(mf.date) "\
            f"ORDER BY mpp.date;"
        monthly_payment_list = database.execute_all(sql)

        # 납부해야 할 회비를 확인하기 위해 필요한 회원 정보 불러오기
        sql = f"SELECT level, grade FROM users WHERE id = {user_id};"
        user_info = database.execute_one(sql)
        # 납부해야 할 회비 금액
        amount = get_amount(user_info)
        database.close()

        # 입부 전(납부를 처음으로 시작한 달 이전엔 아직 입부하지 않은 것으로 간주)의 데이터 제거
        filtered_list = []
        for monthly_payment in monthly_payment_list:
            if monthly_payment['payment_date'] or filtered_list:
                filtered_list.append(monthly_payment)
        monthly_payment_list = filtered_list

        if not monthly_payment_list: # 납부 내역이 없을 때의 처리
            return [], 200
        else:
            for idx, monthly_payment in enumerate(monthly_payment_list):
                # 납부 상태 설정
                monthly_payment_list[idx]['state'] = get_payment_state(monthly_payment)

                # 납부 금액 설정
                if not monthly_payment_list[idx]['amount']:
                    monthly_payment_list[idx]['amount'] = amount

                # 각 날짜를 문자열로 변환
                monthly_payment_list[idx]['date'] = monthly_payment['date'].strftime('%Y-%m-%d')
                monthly_payment_list[idx]['start_day'] = monthly_payment['start_day'].strftime('%Y-%m-%d')
                monthly_payment_list[idx]['end_day'] = monthly_payment['end_day'].strftime('%Y-%m-%d')
                if monthly_payment_list[idx]['payment_date']:
                    monthly_payment_list[idx]['payment_date'] = monthly_payment['payment_date'].strftime('%Y-%m-%d')

            return monthly_payment_list, 200