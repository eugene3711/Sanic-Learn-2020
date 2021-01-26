from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchMessageDto
from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBMessageNotExistsException, DBDataException, DBIntegrityException
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicMessageNotFound, SanicDBException


class MessageEndpoint(BaseEndpoint):

    async def method_get(self, request: Request, body: dict, session: DBSession, message_id: int, *args, **kwargs) -> BaseHTTPResponse:

        try:
            message = message_queries.get_message(session, message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')  # change

        response_model = ResponseMessageDto(message)

        return await self.make_response_json(status=200, body=response_model.dump())



    async def method_patch(
            self, request: Request, body: dict, session: DBSession,  message_id: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_model = RequestPatchMessageDto(body)
        # change only user's messages, not all of them
        try:
            message = message_queries.patch_message(session, request_model, message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')  #change

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
            user = message_queries.delete_message(session, message_id)
        except DBMessageNotExistsException:
            raise SanicUserNotFound('User not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)
