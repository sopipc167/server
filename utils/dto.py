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

    response_user_list = api.model('model_user_list', {
        'user_list': fields.List(fields.Nested(model_user), description='회원 목록')
    })

    response_message = api.model('response_message', {
        'message': fields.String(description='결과 메시지')
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

class adminProductDTO: #임원진 물품 DTO
    api = Namespace('product',description='임원진 물품관리')
    admin_product_response = api.model('admin_product_response',{ # 기본적으로 응답의 상태를 메세지로 출력하는 모델
        'message':fields.String(description='응답 결과')
    })
    admin_product_response_all = api.inherit('admin_product_response_all',admin_product_response,{ # 정상적으로 결과를 출력했을 시의 모델
        'message':fields.String('성공적으로 물품을 불러왔어요'),
        'is_available':fields.Boolean(description='물품 이용 가능 여부'),
        'code':fields.String(description='물품 식별 code'),
        'name':fields.String(description='물품 이름'),
        'category':fields.String(description='물품 종류'),
        'location':fields.String(description='물품 위치'),
        'detail_location':fields.String(description='물품 상세 위치'),
        'model_name':fields.String(description='물품 모델명'),
        'status':fields.String(description='물품 상태'),
        'author':fields.String(description='물품 주인 혹은 기부자'),
        'publisher':fields.String(description='출판사'),
        'user_id':fields.String(description='대여 회원 id(대여 물품 아닐시 null)'),
        'deadline':fields.Date(description='반납기한(대여 물품 아닐시 null)'),
        'rent_day':fields.Date(description='대여일시(대여 물품 아닐시 null)'),
        'return_day':fields.Date(description='반납한 날짜(대여 물품 아닐시 null)'),
    })
    no_product_find = api.inherit('no_product_find',admin_product_response,{ # 찾는 물품이 존재하지 않았을 때의 모델
        'message':fields.String(" 해당 물품이 존재하지 않아요.")
    })
    internal_error = api.inherit('internal_error', admin_product_response, { # 내부 서버에 문제가 생겼을 시의 모델
        'message': fields.String("내부 서버에 문제가 발생했어요.")
    })

class feedbackDTO:  # 피드백 DTO
    api = Namespace('feedback', description='임원진 물품관리')
    feedback_response = api.model('feedback_response', {
        'message': fields.String(description='응답결과')
    })
    feedback_response_all = api.inherit('feedback_response_all', feedback_response, {
        'message': '성공적으로 모든 물품을 불러왔어요.',
        'code': fields.Integer(description='피드백을 구분하기 위한 식별자'),
        'user_id': fields.String(description='피드백을 작성한 유저 식별자'),
        'is_annoy': fields.Integer(description='익명인지 아닌지를 판별하는 데이터베이스'),
        'title': fields.String(description='피드백 글 제목'),
        'content': fields.String(description='피드백 글 내용'),
        'is_answered': fields.Integer(description='피드백 답변 여부')
    })
    feedback_response_search = api.inherit('feedback_response_search', feedback_response, {
        'message': '성공적으로 검색된 물품을 불러왔어요',
        'user_id': fields.String(description='피드백을 작성한 유저 식별자'),
        'is_annoy': fields.Integer(description='익명인지아닌지를 판별하는 데이터베이스'),
        'title': fields.String(description='피드백 글 제목'),
        'content': fields.String(description='피드백 글 내용'),
        'is_answered': fields.Integer(description='피드백 답변 여부')
    })
    not_qualified = api.inherit('not_qualified', feedback_response, {
        'message': '피드백을 볼 수 없는 권한이 없어요.'
    })
    no_feedback_found = api.inherit('not_qualified', feedback_response, {
        'message': '생성된 피드백이 하나도 없어요'
    })
    already_answered = api.inherit('already_answered', feedback_response, {
        'message': '이미 답변된 피드백이에요.'
    })
    invalid_feedback = api.inherit('invalid_feedback', feedback_response, {
        'message': '존재하지 않는 피드백이에요.'
    })
    no_title = api.inherit('no_title', feedback_response, {
        'message': '제목을 입력해주세요'
    })
    no_contents = api.inherit('no_contents', feedback_response, {
        'message': '내용을 입력해주세요'
    })
    post_sucess = api.inherit('post_sucess', feedback_response, {
        'message': "피드백이 성공적으로 작성되었어요"
    })