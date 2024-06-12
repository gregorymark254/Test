from flask import current_app as app
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError

from auth.helper import add_token, revoke_token, is_token_revoked
from extensions import db, pwd_context, jwt
from models.users import User
from schemas.user import UserCreateSchema

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 400

    schema = UserCreateSchema()
    user = schema.load(request.json)
    db.session.add(user)
    db.session.commit()

    return {'msg': 'Registered successfully'}, 201


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 400

    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return {"msg": "Missing email or password"}, 400

    user = User.query.filter_by(email=email).first()
    if not user or not pwd_context.verify(password, user.password):
        return {"msg": "Invalid credentials"}, 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token(access_token)
    add_token(refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}, 200


@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    add_token(access_token)

    return {"access_token": access_token}, 200


@auth_blueprint.route('revoke_access', methods=['DELETE'])
@jwt_required()
def revoke_access():
    jti = get_jwt()['jti']
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    return {'msg': 'Revoke access successful'}, 200


@auth_blueprint.route('revoke_refresh', methods=['DELETE'])
@jwt_required(refresh=True)
def revoke_refresh():
    jti = get_jwt()['jti']
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    return {'msg': 'Revoke refresh successful'}, 200


@jwt.token_in_blocklist_loader
def check_revoked_token(jwt_headers, jwt_payload):
    try:
        return is_token_revoked(jwt_payload)
    except Exception:
        return True


@jwt.user_lookup_loader
def load_user(jwt_headers, jwt_payload):
    user_id = jwt_payload[app.config['JWT_IDENTITY_CLAIM']]
    return User.query.get(user_id)


@auth_blueprint.errorhandler(ValidationError)
def handle_mashmellow_error(e):
    return jsonify(e.messages), 400
