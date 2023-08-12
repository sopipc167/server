from flask import Blueprint
from flask_restx import Api
from api.admin.accounting.accounting import accounting

admin = Blueprint('admin', __name__, url_prefix='/admin')
api = Api(admin)

api.add_namespace(accounting, '/accounting')