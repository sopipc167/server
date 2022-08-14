from flask import Flask
from flask_restx import Api
from api.auth.oauth import oauth

app = Flask(__name__)
api = Api(app)

api.add_namespace(oauth, '/oauth')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)