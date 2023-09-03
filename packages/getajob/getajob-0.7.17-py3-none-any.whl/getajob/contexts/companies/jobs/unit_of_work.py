from datetime import datetime
from getajob.exceptions import MissingRequiredJobFields
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity
from getajob.vendor.algolia.repository import AlgoliaSearchRepository
from getajob.contexts.search.models import JobSearch

from .models import CreateJob, UserCreateJob, Job


class AlgoliaNotSetError(Exception):
    def __init__(self):
        super().__init__("Algolia jobs repository not set")


class JobsUnitOfWork:
    def __init__(
        self,
        job_repo: BaseRepository,
        company_repo: BaseRepository,
        algola_jobs: AlgoliaSearchRepository | None,
    ):
        self.repo = job_repo
        self.company_repo = company_repo
        self.algolia_jobs = algola_jobs

    def create_job(self, company_id: str, data: UserCreateJob) -> Job:
        company_name = self.company_repo.get(company_id).name
        new_job = CreateJob(
            **data.dict(),
            is_live=False,
            company_id=company_id,
            company_name=company_name,
        )
        return self.repo.create(
            new_job, parent_collections={Entity.COMPANIES.value: company_id}
        )

    def post_job(self, company_id: str, job_id: str):
        if not self.algolia_jobs:
            raise AlgoliaNotSetError()

        job_data = self.repo.get(
            job_id, parent_collections={Entity.COMPANIES.value: company_id}
        )
        missing_fields = job_data.get_missing_post_fields()
        if missing_fields:
            raise MissingRequiredJobFields(f"Missing required fields {missing_fields}")

        self.algolia_jobs.create_object(
            object_id=job_data.id,
            object_data=JobSearch(
                id=job_data.id,
                created=datetime.now(),
                updated=datetime.now(),
                job=job_data,
                company_id=company_id,
            ).dict(),
        )
        return self.repo.update(
            job_id,
            data={"is_live": True, "draft": False},
            parent_collections={Entity.COMPANIES.value: company_id},
        )

    def unpost_job(self, company_id: str, job_id: str):
        if not self.algolia_jobs:
            raise AlgoliaNotSetError()

        self.algolia_jobs.delete_object(job_id)
        return self.repo.update(
            job_id,
            data={"is_live": False},
            parent_collections={Entity.COMPANIES.value: company_id},
        )
