from marshmallow import Schema, fields, validates_schema, ValidationError

from api.base import RequestDto


class RequestCreateMessageDtoSchema(Schema):
    message = fields.Str(required=True, allow_none=False)
    recipient = fields.Str(required=True, allow_none=False)

    @validates_schema
    def validate_login(self, data, **kwargs):
        if len(data['message'].strip()) == 0:
            raise ValidationError("Message can't be empty", 'message')
        if len(data['recipient'].strip()) == 0:
            raise ValidationError('Please specify recipient', 'recipient')


class RequestCreateMessageDto(RequestDto, RequestCreateMessageDtoSchema):
    __schema__ = RequestCreateMessageDtoSchema
