from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto
from api.response import ResponseMessageDto
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException

from db.queries import message as message_queries
from db.exceptions import DBDataException, DBIntegrityException, DBMessageCreateException, DBUserNotExistsException

from helpers.auth.token import read_token


class CreateMessageEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)

        uid = read_token(request.headers['authorization'])['uid']

        try:
            db_message = message_queries.create_message(session, request_model, uid)
        except DBUserNotExistsException as e:
            return await self.make_response_json(status=400, message="No such recipient")
        except DBMessageCreateException as e:
            raise SanicDBException(str(e))

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)
