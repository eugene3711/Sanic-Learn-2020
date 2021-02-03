from typing import List

from api.request import RequestCreateMessageDto, RequestPatchMessageDto
from db.database import DBSession
from db.exceptions import DBMessageNotExistsException
from db.models import DBMessage
from .user import get_uid_by_login


def create_message(session: DBSession, message: RequestCreateMessageDto, uid: int) -> DBMessage:

    recipient_id = get_uid_by_login(session=session, login=message.recipient)

    new_message = DBMessage(

        sender_id=uid,
        recipient_id=recipient_id,
        message=message.message

    )

    session.add_model(new_message)

    return new_message


def patch_message(session: DBSession, message: RequestPatchMessageDto, message_id: int) -> DBMessage:

    db_message = session.get_message_by_id(message_id)

    # just 1 field ? subject to refactor
    for attr in message.fields:
        if hasattr(message, attr):
            value = getattr(message, attr)
            setattr(db_message, attr, value)

    return db_message


def get_message(session: DBSession, message_id: int = None) -> DBMessage:
    db_message = None

    if message_id is not None:
        db_message = session.get_message_by_id(message_id)

    if db_message is None:
        raise DBMessageNotExistsException
    return db_message


def delete_message(session: DBSession, message_id: int) -> DBMessage:
    db_message = session.get_message_by_id(message_id)
    db_message.is_delete = True
    return db_message


def get_messages(session: DBSession, uid: int) -> List['DBMessage']:
    return session.get_message_all(uid)


def get_message_author(session: DBSession, message_id: int) -> int:
    author = session.get_message_author(message_id)
    return author
