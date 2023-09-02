from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
    query_collection_group,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection
from getajob.vendor.firestore.models import FirestoreFilters, FirestorePagination

from .models import RecruiterDetails


class RecruiterDetailsRepository(SingleChildRepository[RecruiterDetails]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
    ):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.RECRUITER_DETAILS.value,
                entity_model=RecruiterDetails,
            ),
            required_parent_keys=[
                Entity.COMPANIES.value,
                Entity.RECRUITERS.value,
            ],
        )
        self.request_scope = request_scope

    def get_all_recruiter_details_for_company(
        self, company_id: str
    ) -> list[RecruiterDetails]:
        return query_collection_group(
            db=self.request_scope.db,
            collection_name=Entity.RECRUITER_DETAILS.value,
            filters=[
                FirestoreFilters(
                    field="company_id",
                    operator="==",
                    value=company_id,
                )
            ],
            pagination=FirestorePagination(start_after=None, limit=None),
            entity_model=RecruiterDetails,
        ).data
