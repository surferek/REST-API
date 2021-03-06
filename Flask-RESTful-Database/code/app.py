from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
# customize JWT auth response, include user_id in response body
from flask import jsonify

from datetime import timedelta

from .security import authenticate, identity as identity_function
from .user import UserRegister
from .items import Item, ItemList

app = Flask(__name__)
app.secret_key = 'presti'
api = Api(app)

CONFIG_DEFAULTS = {
    'JWT_DEFAULT_REALM': 'Login Required',
    'JWT_AUTH_URL_RULE': '/login',
    'JWT_AUTH_ENDPOINT': 'jwt',
    'JWT_AUTH_USERNAME_KEY': 'username',
    'JWT_AUTH_PASSWORD_KEY': 'password',
    'JWT_ALGORITHM': 'HS256',
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_EXPIRATION_DELTA': timedelta(seconds=1000),
    'JWT_NOT_BEFORE_DELTA': timedelta(seconds=0),
}
app.config.from_mapping(CONFIG_DEFAULTS)
jwt = JWT(app, authenticate, identity_function)


@jwt.jwt_error_handler
def customized_error_handler(error):
 return jsonify({
 'message': error.description,
 'code': error.status_code
 }), error.status_code


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
 return jsonify({
 'access_token': access_token.decode('utf-8'),
 'user_id': identity.id
 })


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000)
