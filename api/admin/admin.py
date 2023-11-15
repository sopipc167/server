from flask import Blueprint
from flask_restx import Api
from api.admin.accounting.accounting import accounting
from api.admin.product.product import product
from api.admin.notification.notification import notification
from api.admin.attendance.attendance import attendance


admin = Blueprint('admin', __name__, url_prefix='/admin')



authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(admin, authorizations=authorizations)

api.add_namespace(accounting, '/accounting')
api.add_namespace(product, '/product')
api.add_namespace(notification, '/notification')
api.add_namespace(attendance, '/attendance')

