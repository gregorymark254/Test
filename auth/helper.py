from datetime import datetime

from flask_jwt_extended import decode_token

from flask import current_app as app
from sqlalchemy.exc import NoResultFound

from extensions import db
from models import TokenBlogList


def add_token(encoded_token):
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_id = decoded_token[app.config.get("JWT_IDENTITY_CLAIM")]
    expires = datetime.fromtimestamp(decoded_token['exp'] / 1000)

    db_token = TokenBlogList(
        jti=jti,
        token_type=token_type,
        user_id=user_id,
        expires=expires
    )
    db.session.add(db_token)
    db.session.commit()


def revoke_token(token_jti, user_id):
    try:
        token = TokenBlogList.query.filter_by(jti=token_jti, user_id=user_id).one()
        token.revoked_at = datetime.utcnow()
        db.session.commit()
    except NoResultFound:
        raise Exception('Token jti not found')


def is_token_revoked(jwt_payload):
    jti = jwt_payload['jti']
    user_id = jwt_payload[app.config.get("JWT_IDENTITY_CLAIM")]
    try:
        token = TokenBlogList.query.filter_by(jti=jti, user_id=user_id).one()
        return token.revoked_at is not None
    except NoResultFound:
        raise Exception('Token jti not found')