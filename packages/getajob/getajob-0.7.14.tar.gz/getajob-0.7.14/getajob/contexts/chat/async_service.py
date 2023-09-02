from getajob.abstractions.models import UserAndDatabaseConnection, ProcessedAsyncMessage
from getajob.contexts.chat.repository import ChatRepository
from getajob.vendor.mailgun.repository import MailGunRepository


class AsyncronousChatService:
    def __init__(self, mailgun: MailGunRepository):
        self.mailgun = mailgun

    async def _get_chat(self, chat_id: str, request_scope: UserAndDatabaseConnection):
        return ChatRepository(request_scope=request_scope).get(chat_id)

    async def send_chat_message_as_email(
        self, processed_message: ProcessedAsyncMessage
    ):
        # This is put on hold for now, not important for first release
        raise NotImplementedError
