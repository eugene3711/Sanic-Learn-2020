from marshmallow import Schema, fields, validates_schema, validates, ValidationError

from api.base import RequestDto


class RequestCreateUserDtoSchema(Schema):
    login = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)

    @validates_schema
    def validate_credentials(self, data, **kwargs):
        if len(data['login'].strip()) < 4:
            raise ValidationError('Login must be at least 4 characters', 'login')
        if len(data['password'].strip()) < 6:
            raise ValidationError('Password must be at least 6 characters', 'password')

    @validates('first_name')
    def validate_age(self, data, **kwargs):
        if data.strip() == "":
            raise ValidationError('First name is necessary to provide')


class RequestCreateUserDto(RequestDto, RequestCreateUserDtoSchema):
    __schema__ = RequestCreateUserDtoSchema
