from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchMessageDto
from api.response import ResponseMessageDto

from db.database import DBSession
from db.exceptions import DBMessageNotExistsException, DBDataException, DBIntegrityException
from db.queries import message as message_queries

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicMessageNotFound, SanicDBException, SanicForbidden

from helpers.auth import get_id_from_token


class MessageEndpoint(BaseEndpoint):

    async def method_get(self, request: Request,
                         body: dict,
                         session: DBSession,
                         message_id: int, *args, **kwargs) -> BaseHTTPResponse:

        try:
            message = message_queries.get_message(session, message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')  # change

        if not (message.recipient_id == get_id_from_token(request)) and \
           not (message.sender_id == get_id_from_token(request)):
            raise SanicForbidden('You have no rights to read this message')

        response_model = ResponseMessageDto(message)

        return await self.make_response_json(status=200, body=response_model.dump())



    async def method_patch(
            self, request: Request, body: dict, session: DBSession,  message_id: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        if get_id_from_token(request) != message_queries.get_message_author(session, message_id):
            raise SanicForbidden('You have no rights to edit this message')

        request_model = RequestPatchMessageDto(body)

        try:
            message = message_queries.patch_message(session, request_model, message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(message)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_delete(
            self, request: Request, body: dict, session: DBSession, message_id: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            message = message_queries.delete_message(session, message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        if get_id_from_token(request) != message_queries.get_message_author(session, message_id):
            raise SanicForbidden('You have no rights to delete this message')


        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)
