from concurrent.futures import ThreadPoolExecutor

from getajob.abstractions.models import (
    Entity,
    RepositoryDependencies,
    UserAndDatabaseConnection,
)
from getajob.abstractions.repository import SingleChildRepository
from getajob.contexts.applications.repository import ApplicationRepository
from getajob.contexts.users.saved_jobs.repository import UserSavedJobsRepository
from getajob.contexts.users.repository import UserRepository
from getajob.vendor.firestore.models import FirestorePagination

from .models import UserDashboard
from .unit_of_work import UserDashboardUnitOfWork


class UserDashboardRepository(SingleChildRepository):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        self.request_scope = request_scope
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.USER_DASHBOARD.value,
                entity_model=UserDashboard,
            ),
            required_parent_keys=[Entity.USERS.value],
        )

    def get_and_save_updated_user_dashboard(self, user_id: str) -> UserDashboard:
        updated_dashboard = UserDashboardUnitOfWork(
            ApplicationRepository(request_scope=self.request_scope, kafka=None),
            UserSavedJobsRepository(request_scope=self.request_scope),
        ).get_user_dashboard(user_id)
        self.set_sub_entity(
            data=updated_dashboard,
            parent_collections={Entity.USERS.value: user_id},
        )
        return updated_dashboard

    def update_all_user_dashboards(self):
        user_repo = UserRepository(request_scope=self.request_scope, kafka=None)
        all_users = user_repo.query(pagination=FirestorePagination(limit=None)).data
        with ThreadPoolExecutor() as executor:
            for user in all_users:
                executor.submit(
                    UserDashboardRepository(
                        request_scope=self.request_scope
                    ).get_and_save_updated_user_dashboard,
                    user.id,
                )
