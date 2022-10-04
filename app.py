from flask import Flask
from flask_restx import Api
from api.auth.oauth import oauth
from api.user.user import user

app = Flask(__name__)
api = Api(app)

api.add_namespace(oauth, '/oauth')
api.add_namespace(user, '/user')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
