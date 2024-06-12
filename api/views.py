from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from api.resources.user import UserList, UserResourse

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, errors=blueprint.errorhandler)

api.add_resource(UserList, '/users')
api.add_resource(UserResourse, '/users/<int:user_id>')


@blueprint.errorhandler(ValidationError)
def handle_mashmellow_error(e):
    return jsonify(e.messages), 400