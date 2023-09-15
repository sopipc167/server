from flask import Blueprint
from flask_restx import Api
from api.admin.accounting.accounting import accounting
from api.admin.product.admin_product import admin_product

admin = Blueprint('admin', __name__, url_prefix='/admin')
api = Api(admin)

api.add_namespace(accounting, '/accounting')
api.add_namespace(admin_product, '/admin_product')