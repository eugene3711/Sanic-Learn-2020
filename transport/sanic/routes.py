from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        endpoints.HealthEndpoint(
            config=config, context=context, uri='/', methods=('GET', 'POST'),
        ),
        endpoints.CreateUserEndpoint(
            config, context, uri='/user', methods=['POST'],
        ),
        endpoints.AuthUserEndpoint(
            config, context, uri='/auth', methods=['POST'],
        ),
        endpoints.UserEndpoint(
            config, context, uri='/user/<uid:int>', methods=['GET', 'PATCH', 'DELETE'], auth_required=True,
        ),
        endpoints.AllUserEndpoint(
            config, context, uri='/user/all', methods=['GET'], auth_required=True,
        ),
        endpoints.CreateMessageEndpoint(
            config, context, uri='msg', methods=['POST'], auth_required=True,
        ),
        endpoints.AllMessagesEndpoint(
            config, context, uri='msg', methods=['GET'], auth_required=True,
        ),
        endpoints.MessageEndpoint(
            config, context, uri='msg/<message_id:int>', methods=['GET', 'PATCH', 'DELETE'], auth_required=True,
        )
    )
