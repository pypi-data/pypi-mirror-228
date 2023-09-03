from datetime import datetime
from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class UserCreateChatMessage(BaseModel):
    user_id: str
    message: str
    message_time: datetime = datetime.now()


class UpdateChatMessage(BaseModel):
    is_recruiter: bool | None
    is_read: bool | None = None
    read_at: datetime | None = None
    email_sent: bool | None = None


class ChatMessage(UserCreateChatMessage, UpdateChatMessage, BaseDataModel):
    ...
