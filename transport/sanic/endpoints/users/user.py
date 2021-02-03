from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchUserDto
from api.response import ResponseUserDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException, DBDataException, DBIntegrityException
from db.queries import user as user_queries
from helpers.auth import read_token, get_id_from_token
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound, SanicDBException, SanicForbidden


class UserEndpoint(BaseEndpoint):

    async def method_get(self, request: Request, body: dict, session: DBSession, uid: int, *args, **kwargs) -> BaseHTTPResponse:

        try:
            message = user_queries.get_user(session, uid=uid)
        except DBUserNotExistsException:
            raise SanicUserNotFound('User not found')  # change

        response_model = ResponseUserDto(message)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, uid: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        if uid != get_id_from_token(request):
            raise SanicForbidden('You have no rights to edit this user')

        request_model = RequestPatchUserDto(body)

        try:
            user = user_queries.patch_user(session, request_model, uid)
        except DBUserNotExistsException:
            raise SanicUserNotFound('User not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseUserDto(user)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_delete(
            self, request: Request, body: dict, session: DBSession, uid: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        if uid != get_id_from_token(request):
            raise SanicForbidden('You have no rights to delete this user')

        try:
            user = user_queries.delete_user(session, uid)
        except DBUserNotExistsException:
            raise SanicUserNotFound('User not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)
