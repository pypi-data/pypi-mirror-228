from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic, KafkaJobsEnum
from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection
from getajob.vendor.algolia.repository import AlgoliaSearchRepository
from getajob.contexts.companies.repository import CompanyRepository

from .models import Job, UserCreateJob
from .unit_of_work import JobsUnitOfWork


class JobsRepository(MultipleChildrenRepository[Job]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
        kafka: KafkaProducerRepository | None,
        algolia_jobs: AlgoliaSearchRepository | None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.jobs, message_type_enum=KafkaJobsEnum
        )
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.JOBS.value,
                entity_model=Job,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
            ),
            required_parent_keys=[Entity.COMPANIES.value],
        )
        self.request_scope = request_scope
        self.algolia_jobs = algolia_jobs
        self.company_repo = CompanyRepository(request_scope=request_scope, kafka=None)

    def create_job(self, company_id: str, job: UserCreateJob):
        return JobsUnitOfWork(self, self.company_repo, self.algolia_jobs).create_job(
            company_id, job
        )

    def post_job(self, company_id: str, job_id: str):
        return JobsUnitOfWork(self, self.company_repo, self.algolia_jobs).post_job(
            company_id, job_id
        )

    def unpost_job(self, company_id: str, job_id: str):
        return JobsUnitOfWork(self, self.company_repo, self.algolia_jobs).unpost_job(
            company_id, job_id
        )
