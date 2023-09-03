from concurrent.futures import ThreadPoolExecutor

from getajob.abstractions.models import (
    Entity,
    RepositoryDependencies,
    UserAndDatabaseConnection,
)
from getajob.abstractions.repository import SingleChildRepository
from getajob.contexts.companies.jobs.repository import JobsRepository
from getajob.contexts.applications.repository import ApplicationRepository
from getajob.contexts.companies.repository import CompanyRepository
from getajob.contexts.companies.saved_candidates.repository import (
    CompanySavesCandidateRepository,
)
from getajob.vendor.firestore.models import FirestorePagination

from .models import CompanyDashboard
from .unit_of_work import CompanyDashboardUnitOfWork


class CompanyDashboardRepository(SingleChildRepository):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        self.request_scope = request_scope
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.COMPANY_DASHBOARD.value,
                entity_model=CompanyDashboard,
            ),
            required_parent_keys=[Entity.COMPANIES.value],
        )

    def get_and_save_updated_company_dashboard(
        self, company_id: str
    ) -> CompanyDashboard:
        updated_dashboard = CompanyDashboardUnitOfWork(
            JobsRepository(
                request_scope=self.request_scope, kafka=None, algolia_jobs=None
            ),
            ApplicationRepository(request_scope=self.request_scope, kafka=None),
            CompanySavesCandidateRepository(request_scope=self.request_scope),
        ).get_company_dashboard(company_id)
        self.set_sub_entity(
            data=updated_dashboard,
            parent_collections={Entity.COMPANIES.value: company_id},
        )
        return updated_dashboard

    def update_all_company_dashboards(self):
        company_repo = CompanyRepository(request_scope=self.request_scope, kafka=None)
        all_companies = company_repo.query(
            pagination=FirestorePagination(limit=None)
        ).data
        with ThreadPoolExecutor() as executor:
            for company in all_companies:
                executor.submit(
                    CompanyDashboardRepository(
                        request_scope=self.request_scope
                    ).get_and_save_updated_company_dashboard,
                    company_id=company.id,
                )
