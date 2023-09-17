from flask_restx import Namespace, fields
class feedbackDTO:
    api= Namespace('feedback',description='임원진 물품관리')
    feedback_response = api.model('feedback_response',{
        'message': fields.String(description='응답결과')
    })
    feedback_response_all = api.inherit('feedback_response_all',feedback_response,{
        'message':'성공적으로 모든 물품을 불러왔습니다.',
        'code':fields.Integer(description='피드백을 구분하기 위한 식별자'),
        'user_id':fields.String(description='피드백을 작성한 유저 식별자'),
        'is_annoy':fields.Integer(description='익명인지아닌지를 판별하는 데이터베이스'),
        'title':fields.String(description='피드백 글 제목'),
        'content':fields.String(description='피드백 글 내용'),
        'is_answered':fields.Integer(description='피드백 답변 여부')
    })
    feedback_response_search = api.inherit('feedback_response_search',feedback_response,{
        'message': '성공적으로 검색된 물품을 불러왔습니다.',
        'user_id': fields.String(description='피드백을 작성한 유저 식별자'),
        'is_annoy': fields.Integer(description='익명인지아닌지를 판별하는 데이터베이스'),
        'title': fields.String(description='피드백 글 제목'),
        'content': fields.String(description='피드백 글 내용'),
        'is_answered': fields.Integer(description='피드백 답변 여부')
    })
    not_qualified = api.inherit('not_qualified',feedback_response,{
        'message':'피드백을 볼 수 없는 권한이 없어요.'
    })
    no_feedback_found = api.inherit('not_qualified', feedback_response,{
        'message':'생성된 피드백이 하나도 없어요'
    })
    already_answered = api.inherit('already_answered',feedback_response,{
        'message':'이미 답변된 피드백입니다.'
    })
    invalid_feedback = api.inherit('invalid_feedback',feedback_response,{
        'message':'존재하지 않는 피드백입니다.'
    })
    no_title = api.inherit('no_title',feedback_response,{
        'message':'제목을 입력해주세요'
    })
    no_contents = api.inherit('no_contents',feedback_response,{
        'message':'내용을 입력해주세요'
    })
    post_sucess = api.inherit('post_sucess',feedback_response,{
        'message':"피드백이 성공적으로 작성되었습니다"
    })