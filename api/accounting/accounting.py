from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database
from datetime import datetime, date

accounting = Namespace('accounting')

# 회비 category
MEMBERSHIP_FEE_CATEGORY = {1: '납부 완료', 2: '납부 완료', 3: '납부 지연', 4: '미납'}

# 회계 내역 category(내역 유형)
ACCOUNTING_CATEGORY = {0: '문의 불가', 1: '문의 가능'}

# payment_method(결제 수단)
PAYMENT_METHOD = {0: '통장', 1: '금고'}

# index 데이터를 문자열로 변경
def convert_to_string(dictionary, index):
    return dictionary.get(index, None)

# 문자열 데이터를 index로 변경
def convert_to_index(dictionary, string):
    for key, value in dictionary.items():
        if value == string:
            return key
    return None

# DB에있는 모든 내역의 금액의 합 계산하기
def get_total_amount(database):
    sql = "SELECT sum(amount) as total FROM accountings;" 
    accounting = database.execute_one(sql)
    return int(accounting['total'])

@accounting.route('/<int:user_id>')
class AccountingUserAPI(Resource):
    # 회원의 월별 회비 납부 내역 얻기
    def get(self, user_id):
        # 금월 및 작년 6월 날짜 구한 뒤 문자열로 변환 ('YYYY-MM-01' 형식)
        current_month = date(datetime.today().year, datetime.today().month, 1)
        start_month = date(current_month.year - 1, 6, 1)
        current_month.strftime('%Y-%m-%d')
        start_month.strftime('%Y-%m-%d')

        print(current_month, start_month)

        database = Database()

        # DB에서 user_id값에 맞는 월별 회비 납부 내역 불러오기 (작년 6월부터 현재 달까지)
        sql = f"SELECT date, amount, category FROM membership_fees "\
            f"WHERE user_id = {user_id} "\
            f"and date between '{start_month}' and '{current_month}';"
        monthly_payment_list = database.execute_all(sql)

        # 금월 회비 납부 기간 불러오기
        sql = f"SELECT start_date, end_date FROM monthly_payment_periods "\
            f"WHERE date = '{current_month}';"
        payment_period = database.execute_one(sql)
        
        # 계좌 내의 총 금액 불러오기
        total_amount = get_total_amount(database)

        database.close()

        # 납부 기간 문자열로 변환
        if payment_period:
            payment_period['start_date'] = payment_period['start_date'].strftime('%Y-%m-%d')
            payment_period['end_date'] = payment_period['end_date'].strftime('%Y-%m-%d')

        result_data = {'monthly_payment_list': monthly_payment_list, 'payment_period': payment_period, 'total_amount': total_amount}

        if not monthly_payment_list: # 납부 내역이 없을 때의 처리
            return result_data, 200
        else:
            for idx, monthly_payment in enumerate(monthly_payment_list):
                # date 및 category를 문자열로 변환
                monthly_payment_list[idx]['date'] = monthly_payment['date'].strftime('%Y-%m-%d')
                monthly_payment_list[idx]['category'] = convert_to_string(MEMBERSHIP_FEE_CATEGORY, monthly_payment['category'])

            return result_data, 200
    
@accounting.route('/list')
class AccountingListAPI(Resource):
    # 회비 내역 목록 얻기
    def get(self):
        database = Database()

        # DB에서 전체 회비 내역 목록 불러오기
        sql = "SELECT * FROM accountings;"
        accounting_list = database.execute_all(sql)

        # 계좌 내의 총 금액 불러오기
        total_amount = get_total_amount(database)

        database.close()

        result_data = {'accounting_list': accounting_list, 'total_amount': total_amount}

        if not accounting_list: # 회비 내역이 없을 때 처리
            return result_data, 200
        else:
            for idx, accounting in enumerate(accounting_list):
                # date 및 category, payment_method를 문자열로 변환
                accounting_list[idx]['date'] = accounting['date'].strftime('%Y-%m-%d')
                accounting_list[idx]['category'] = convert_to_string(ACCOUNTING_CATEGORY, accounting['category'])
                accounting_list[idx]['payment_method'] = convert_to_string(PAYMENT_METHOD, accounting['payment_method'])
            return result_data, 200