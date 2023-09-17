from flask_restx import Namespace, fields
class adminProductDTO:
    api = Namespace('admin_product',description='임원진 물품관리')
    admin_product_response = api.model('admin_product_response',{ #기본적으로 응답의 상태를 메세지로 출력하는 모델
        'message':fields.String(description='응답 결과')
    })
    admin_product_response_all = api.inherit('admin_product_response_all',admin_product_response,{ #정상적으로 결과를 출력했을 시의 모델
        'message':fields.String('성공적으로 물품을 불러왔습니다'),
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
    no_product_find = api.inherit('no_product_find',admin_product_response,{ #찾는 물품이 존재하지 않았을 때의 모델
        'message':fields.String(" 해당 물품이 존재하지 않습니다.")
    })
    internal_error = api.inherit('internal_error', admin_product_response, { #내부 서버에 문제가 생겼을 시의 모델
        'message': fields.String("내부 서버에 문제가 발생했습니다.")
    })