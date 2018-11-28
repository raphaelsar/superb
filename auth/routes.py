from flask.blueprints import Blueprint

from .views.api import AuthAPI

# Routes for API
api = Blueprint('api', __name__, url_prefix='/auth')

auth_api = AuthAPI.as_view('auth_api')
api.add_url_rule('/<uuid>/<application_uuid>', view_func=auth_api,
                 methods=['GET'])
