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

    response_data_with_code = api.inherit('response_data_with_code', response_data, {
        'code': fields.Integer(description='상태 코드', example=200)
    })

    response_message = api.model('response_message', {
        'message': fields.String(description='결과 메시지', example="회원의 출석 인증 정보를 수정했어요 :)")
    })

    response_message_with_code = api.inherit('response_message', response_message, {
        'code': fields.Integer(description='상태 코드', example=200)
    })

    query_user_id = api.parser().add_argument(
        'user_id', type=str, help='유저 ID'
    )

class feedbackDTO: # 피드백 DTO
    api = Namespace('feedback', description='임원진 물품관리')
    feedback_response = api.model('feedback_response', {
        'message': fields.String(description='응답결과')
    })
    feedback_response_all = api.inherit('feedback_response_all', feedback_response, {
        'message': '성공적으로 모든 물품을 불러왔습니다.',
        'code': fields.Integer(description='피드백을 구분하기 위한 식별자'),
        'user_id': fields.String(description='피드백을 작성한 유저 식별자'),
        'is_annoy': fields.Integer(description='익명인지 아닌지를 판별하는 데이터베이스'),
        'title': fields.String(description='피드백 글 제목'),
        'content': fields.String(description='피드백 글 내용'),
        'is_answered': fields.Integer(description='피드백 답변 여부')
    })
    feedback_response_search = api.inherit('feedback_response_search', feedback_response, {
        'message': '성공적으로 검색된 물품을 불러왔습니다.',
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