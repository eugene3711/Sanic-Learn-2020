from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.sanic.base import SanicEndpoint
from helpers.auth.token import read_token

class HealthEndpoint(SanicEndpoint):
    async def method_get(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        response = {
            'headers': request.headers['authorization'],
            'id': read_token(request.headers['authorization'])
        }
        return await self.make_response_json(body=response, status=200)

    async def method_post(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.make_response_json(body=body, status=200)
