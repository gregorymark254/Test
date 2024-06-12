from marshmallow.fields import String
from marshmallow import validate, validates_schema, ValidationError

from extensions import ma
from models.users import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    name = String(required=True, validate=validate.Length(min=1), error_messages={'required': 'Name is required'})
    email = String(required=True, validate=validate.Email())

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get('email')

        if User.query.filter_by(email=email).count():
            raise ValidationError(f'Email {email} already registered')

    class Meta:
        model = User
        load_instance = True
        exclude = ['id']
