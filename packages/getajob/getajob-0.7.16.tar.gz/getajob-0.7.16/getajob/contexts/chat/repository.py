from getajob.vendor.firestore.models import FirestoreFilters
from getajob.abstractions.models import Entity
from getajob.abstractions.repository import (
    ParentRepository,
    RepositoryDependencies,
)
from getajob.contexts.companies.recruiters.repository import RecruiterRepository
from getajob.contexts.applications.repository import ApplicationRepository
from getajob.contexts.users.repository import UserRepository
from getajob.abstractions.models import UserAndDatabaseConnection

from .models import UserCreateChat, Chat
from .unit_of_work import CreateChatUnitOfWork


class ChatRepository(ParentRepository[Chat]):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.CHAT.value,
                entity_model=Chat,
            )
        )
        self.request_scope = request_scope

    def create_new_chat(self, create_chat: UserCreateChat):
        return CreateChatUnitOfWork(
            application_repository=ApplicationRepository(
                request_scope=self.request_scope, kafka=None
            ),
            recruiter_repository=RecruiterRepository(request_scope=self.request_scope),
            user_repository=UserRepository(
                request_scope=self.request_scope, kafka=None
            ),
            chat_repository=self,
        ).create_new_chat(create_chat)

    def get_all_chats_user_is_part_of(self, user_id: str):
        return self.query(
            filters=[
                FirestoreFilters(
                    field="applicant_user_id", operator="==", value=user_id
                )
            ]
        )

    def get_all_chats_compny_is_part_of(self, company_id: str):
        return self.query(
            filters=[
                FirestoreFilters(field="company_id", operator="==", value=company_id)
            ]
        )
