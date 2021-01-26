from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response import ResponseMessageDto
from db.database import DBSession
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint

from helpers.auth import read_token


class AllMessagesEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, *args, **kwargs
    ) -> BaseHTTPResponse:

        uid = read_token(request.headers['authorization'])['uid']
        db_message = message_queries.get_messages(session, uid)
        response_model = ResponseMessageDto(db_message, many=True)

        return await self.make_response_json(status=200, body=response_model.dump())
