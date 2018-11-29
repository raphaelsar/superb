import logging
import uuid
from flask import request, Response
from flask.views import MethodView
from webargs import fields, ValidationError
from webargs.flaskparser import use_kwargs
from auth.models import User


def validate_uuid_regex(value):
    try:
        uuid.UUID(value)
    except ValueError:
        raise ValidationError('Invalid Application UUID', status_code=403, headers=None)

logger = logging.getLogger(__name__)

auth_args = {
    "application_uuid": fields.Str(validate=validate_uuid_regex),
    "uuid": fields.Str(validate=validate_uuid_regex)
}


class AuthAPI(MethodView):
    def __init__(self):
        self.uuid = None

    @use_kwargs(auth_args, locations=("view_args",))  # Injects args dictionary
    def get(self, **kwargs):
        """"
        Return an access token for uuid user, given an application uuid.
        """
        status_code = 400
        body_response = {
            "status": 'error',
            "message": "invalid params"
        }
        application_uuid = kwargs.get('application_uuid', None)

        if application_uuid is None:
            body_response.update({"message": "application_uuid must be informed"})
            return 'b'

        user_uuid = kwargs.get('uuid', None)

        if user_uuid is None:
            # gerar token anonimo
            return application_uuid
            # gerar token com as infos do usuário

    def post(self, **kwargs):
        """"
        Create new user given uuid, password and application uuid.
        Return an access token
        """
        # password = md5.new(request.values.get('password')).digest()
        # ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        #
        # user = User(kwargs);

        return 'a'

    def create_response(body_response, status_code):
        response = Response(body_response, status=status_code, mimetype='application/json')
        response.cache_control.private = True
        response.cache_control.must_revalidate = True
        return response
