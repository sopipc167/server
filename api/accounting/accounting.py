from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from datetime import datetime

accounting = Namespace('accounting')

# category(내역 유형)
ACCOUNTING_CATEGORY = {0: '문의 불가', 1: '문의 가능'}

# payment_method(결제 수단)
PAYMENT_METHOD = {0: '통장', 1: '금고'}

# category를 문자열로 변환
def ac_int_to_str(category):
    return ACCOUNTING_CATEGORY.get(category, None)

# category를 index로 변환
def ac_str_to_int(category):
    for key, value in ACCOUNTING_CATEGORY.items():
        if value == category:
            return key
    return None

# payment_method를 문자열로 변환
def pm_int_to_str(payment_method):
    return PAYMENT_METHOD.get(payment_method, None)

# payment_method를 index로 변환
def pm_str_to_int(payment_method):
    for key, value in PAYMENT_METHOD.items():
        if value == payment_method:
            return key
    return None

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
        
# 회원 등급 및 학년에 따른 회비 반환
def get_amount(user_info):
    if user_info['level'] == 0 and user_info['grade'] == 4: 
        return 3000
    else:
        return 5000

@accounting.route('/<int:user_id>')
class AccountingUserAPI(Resource):
    # 회원의 월별 회비 납부 내역 얻기
    def get(self, user_id):
        database = Database()

        # DB에서 user_id값에 맞는 월별 회비 납부 내역 불러오기
        sql = f"SELECT mpp.date, start_day, end_day, mf.date as payment_date, amount "\
            f"FROM monthly_payment_periods mpp "\
            f"LEFT JOIN membership_fees mf "\
            f"ON mf.user_id = {user_id} and year(mpp.date) = year(mf.date) and month(mpp.date) = month(mf.date) "\
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
        
@accounting.route('/total')
class AccountingTotalAPI(Resource):
    # 현재 계좌 내의 총 금액 얻기
    def get(self):
        # DB에있는 모든 내역의 금액의 합 계산하기
        database = Database()
        sql = "SELECT sum(amount) as total FROM accountings" 
        accounting = database.execute_one(sql)
        database.close()
        accounting['total'] = int(accounting['total'])

        return accounting, 200
    
@accounting.route('/list')
class AccountingListAPI(Resource):
    # 회비 내역 목록 얻기
    def get(self):
        # DB에서 전체 회비 내역 목록 불러오기
        database = Database()
        sql = "SELECT * FROM accountings"
        accounting_list = database.execute_all(sql)
        database.close()

        if not accounting_list: # 회비 내역이 없을 때 처리
            return [], 200
        else:
            for idx, accounting in enumerate(accounting_list):
                # date 및 category, payment_method를 문자열로 변환
                accounting_list[idx]['date'] = accounting['date'].strftime('%Y-%m-%d')
                accounting_list[idx]['category'] = ac_int_to_str(accounting['category'])
                accounting_list[idx]['payment_method'] = pm_int_to_str(accounting['payment_method'])
            return accounting_list, 200