from flask import Flask
from flask_restx import Api
from api.auth.oauth import oauth
from api.user.user import user
from api.product.product import product
from api.project.project import project
from api.seminar.seminar import seminar
from api.warning.warning import warning
from api.accounting.accounting import accounting
from api.home.home import home
from api.admin.admin import admin

app = Flask(__name__)
api = Api(app)

api.add_namespace(oauth, '/oauth')
api.add_namespace(user, '/user')
api.add_namespace(product, '/product')
api.add_namespace(project, '/project')
api.add_namespace(seminar, '/seminar')
api.add_namespace(warning, '/warning')
api.add_namespace(accounting, '/accounting')
api.add_namespace(home, '/home')

app.register_blueprint(admin)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
