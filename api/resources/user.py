from flask import request, jsonify
from flask_restful import Resource

from extensions import db
from models.users import User
from schemas.user import UserSchema


class UserList(Resource):
    def get(self):
        users = User.query.all()
        schema = UserSchema(many=True)
        return {'users': schema.dump(users)}

    def post(self):
        schema = UserSchema()
        validate_data = schema.load(request.json)

        user = User(**validate_data)
        db.session.add(user)
        db.session.commit()

        return {"msg": "user created"}, 201


class UserResourse(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)

        return jsonify(user=user)

    def put(self, user_id):
        schema = UserSchema(partial=True)

        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)
        db.session.add(user)
        db.session.commit()

        return {"msg": "user updated"}, 201

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"msg": "user deleted"}, 201
