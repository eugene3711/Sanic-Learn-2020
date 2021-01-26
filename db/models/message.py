from sqlalchemy import Column, VARCHAR, INTEGER, BOOLEAN

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    sender_id = Column(INTEGER(), nullable=False)
    recipient_id = Column(INTEGER(), nullable=False)
    message = Column(VARCHAR())
    is_delete = Column(BOOLEAN(), nullable=False, default=False)