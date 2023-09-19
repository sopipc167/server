from flask_restx import Namespace, fields

def nullable(field):
    class NullableField(field):
        __schema_type__ = [field.__schema_type__, "null"]
        __schema_example__ = f"nullable {field.__schema_type__}"
    return NullableField

class AttendanceDTO:
    api = Namespace('attendance', description='회원 출석 기능')

    model_attendance = api.model('model_attendance', {
        'date': fields.Date(description='출석 날짜'),
        'category': fields.String(description='회의 종류'),
        'first_auth_start_time': fields.String(description='1차 인증 시작 시간'),
        'first_auth_end_time': fields.String(description='1차 인증 종료 시간'),
        'second_auth_start_time': fields.String(description='2차 인증 시작 시간'),
        'second_auth_end_time': fields.String(description='2차 인증 종료 시간'),
        'state': nullable(fields.String)(description='출석 상태', enum=['출석', '지각', '불참', None]),
        'first_auth_time': nullable(fields.String)(description='1차 인증 시간'),
        'second_auth_time': nullable(fields.String)(description='2차 인증 시간')
    })

    model_record = api.model('model_record', {
        'date': fields.Date(description='출석 일자'),
        'state': fields.String(description='출석 여부')
    })

    model_user_attendance = api.model('model_user_attendance', {
        'user_id': fields.String(description='유저 ID'),
        'state': nullable(fields.String)(description='출석 상태', enum=['출석', '지각', '불참', None]),
        'first_auth_time': nullable(fields.String)(description='1차 인증 시간'),
        'second_auth_time': nullable(fields.String)(description='2차 인증 시간')
    })

    response_data = api.model('response_data', {
        'attendance': fields.Nested(model_attendance, description='금일 참여해야 할 출석 목록'),
        'record_list': fields.List(fields.Nested(model_record), description='최근 4건의 출석 여부')
    })

    response_message = api.model('response_message', {
        'message': fields.String(description='결과 메시지')
    })

    query_user_id = api.parser().add_argument(
        'user_id', type=str, help='유저 ID'
    )

class AdminNotificationDTO:
    api = Namespace('notification', description='임원진 알림 관리')

    model_notification = api.model('model_notification', {
        'id': fields.Integer(description='알림 ID (POST 시에는 유효하지 않습니다.)'),
        'member_category': fields.String(description="알림 대상자 종류", enum=['활동 중인 회원 전체', '활동 중인 정회원', '활동 중인 수습회원', '기타 선택']),
        'time': fields.String(description='알림 시간'),
        'start_date': fields.String(description='시작일'),
        'end_date': fields.String(description='종료일'),
        'day': nullable(fields.String)(description="요일", example='월요일'),
        'cycle': fields.String(description='알림 주기'),
        'message': nullable(fields.String)(description='알림 메시지'),
        'memo': nullable(fields.String)(description='메모'),
        'member_list': fields.List(fields.String, description="알림 대상자 목록('알림 대상자 종류가 '기타 선택'이 아닌 경우 빈 리스트)")
    })

    model_user = api.model('model_user', {
        'id': fields.String(description='회원 ID'),
        'name': fields.String(description='이름'),
        'grade': fields.Integer(description='학년')
    })

    model_payment_period = api.model('model_payment_period', {
        'date': fields.String(description='년/월 (YYYY-MM-01)'),
        'start_date': fields.String(description='납부 시작일'),
        'end_date': fields.String(description='납부 마감일')
    })

    response_message = api.model('response_message', {
        'message': fields.String(description='결과 메시지')
    })

    response_notification_list = api.model('response_notification_list', {
        'notification_list': fields.List(fields.Nested(model_notification), description='알림 목록')
    })

    response_user_list = api.model('response_user_list', {
        'user_list': fields.List(fields.Nested(model_user), description='회원 목록')
    })

    response_payment_period_list = api.model('response_payment_period_list', {
        'payment_period_list': fields.List(fields.Nested(model_payment_period), description='회비 납부 기간 목록')
    })

    query_notification_id = api.parser().add_argument(
        'notification_id', type=str, help='알림 ID'
    )

class AdminAttendanceDTO:
    api = Namespace('attendance', description='임원진 출석 관리')

    model_attendance = api.model('model_attendance', {
        'id': fields.Integer(description='ID'),
        'date': fields.Date(description='출석 날짜'),
        'category': fields.String(description='회의 종류'),
        'first_auth_start_time': nullable(fields.String)(description='1차 인증 시작 시간'),
        'first_auth_end_time': nullable(fields.String)(description='1차 인증 종료 시간'),
        'second_auth_start_time': nullable(fields.String)(description='2차 인증 시작 시간'),
        'second_auth_end_time': nullable(fields.String)(description='2차 인증 종료 시간'),
    })

    model_user = api.model('model_user', {
        'id': fields.String(description='ID'),
        'name': fields.String(description='이름'),
        'grade': fields.String(description='학년'),
        'part_index': fields.Integer(description='소속 파트'),
        'rest_type': fields.String(description='활동 여부'),
        'state': nullable(fields.String)(description='출석 상태', enum=['출석', '지각', '불참', None]),
        'first_auth_time': nullable(fields.String)(description='1차 인증 시간'),
        'second_auth_time': nullable(fields.String)(description='2차 인증 시간')
    })

    model_user_attendance = api.model('model_user_attendance', {
        'user_id': fields.String(description='ID'),
        'state': nullable(fields.String)(description='출석 상태', enum=['출석', '지각', '불참', None]),
        'first_auth_time': nullable(fields.String)(description='1차 인증 시간'),
        'second_auth_time': nullable(fields.String)(description='2차 인증 시간')
    })

    response_attendance = api.model('response_attendance', {
        'date': fields.Date(description='출석 날짜'),
        'first_auth_start_time': fields.String(description='1차 인증 시작 시간'),
        'first_auth_end_time': fields.String(description='1차 인증 종료 시간'),
        'second_auth_start_time': fields.String(description='2차 인증 시작 시간'),
        'second_auth_end_time': fields.String(description='2차 인증 종료 시간')
    })

    response_attendance_with_code = api.inherit('response_attendance_with_code', model_attendance, {
        'code': fields.Integer(description='상태 코드', example=200)
    })

    response_user_list = api.model('model_user_list', {
        'user_list': fields.List(fields.Nested(model_user), description='회원 목록')
    })

    response_user_list_with_code = api.inherit('response_user_list_with_code', response_user_list, {
        'code': fields.Integer(description='상태 코드', example=200)
    })
    
    response_message = api.model('response_message', {
        'message': fields.String(description='결과 메시지')
    })

    response_message_with_code = api.inherit('response_message', response_message, {
        'code': fields.Integer(description='상태 코드', example=200)
    })

    response_user_attendance_with_code = api.inherit('response_user_attendance_with_code', model_user_attendance, {
        'code': fields.Integer(description='상태 코드', example=200)
    })

    query_date = api.parser().add_argument(
        'date', type=str, help='출석 일자'
    )

    query_user_id = api.parser().add_argument(
        'user_id', type=str, help='유저 ID'
    )

    query_attendance_id = api.parser().add_argument(
        'attendance_id', type=int, help='출석 ID'
    )