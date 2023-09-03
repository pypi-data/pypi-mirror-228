"""A weekly summary of job and application summary data"""

import logging
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from cachetools import cached, TTLCache

from getajob.abstractions.models import UserAndDatabaseConnection, Entity
from getajob.abstractions.repository import query_collection
from getajob.vendor.firestore.models import FirestoreFilters, FirestorePagination
from getajob.contexts.companies.repository import CompanyRepository
from getajob.contexts.applications.repository import ApplicationRepository
from getajob.contexts.applications.models import Application
from getajob.contexts.companies.jobs.models import Job
from getajob.contexts.companies.jobs.repository import JobsRepository
from getajob.contexts.companies.recruiters.recruiter_settings.models import (
    RecruiterDetails,
)
from getajob.contexts.users.repository import UserRepository
from getajob.contexts.companies.recruiters.recruiter_settings.repository import (
    RecruiterDetailsRepository,
)
from getajob.vendor.mailgun.repository import MailGunRepository

from .models import WeekdayReport, WeeklyReportData


logger = logging.getLogger(__name__)


class WeeklyApplicationUpdatesService:
    def __init__(self, request_scope: UserAndDatabaseConnection):
        self.request_scope = request_scope
        self.company_repository = CompanyRepository(
            request_scope=request_scope, kafka=None
        )
        self.application_repository = ApplicationRepository(
            request_scope=request_scope, kafka=None
        )
        self.recruiter_details_repository = RecruiterDetailsRepository(
            request_scope=request_scope
        )
        self.jobs_repository = JobsRepository(
            request_scope=request_scope, kafka=None, algolia_jobs=None
        )
        self.user_repository = UserRepository(request_scope=request_scope, kafka=None)
        self.mailgun = MailGunRepository()

    @cached(cache=TTLCache(maxsize=1024, ttl=60))
    def get_recruiter_name_email(self, user_id: str):
        user = self.user_repository.get(user_id)
        return (user.first_name, self.user_repository.get_email_from_user(user=user))

    def get_applications_for_company(self, company_id: str) -> list[Application]:
        return self.application_repository.query(
            filters=[
                FirestoreFilters(field="company_id", operator="==", value=company_id)
            ]
        ).data

    def get_created_jobs_for_company(self, company_id: str) -> list[Job]:
        return query_collection(
            db=self.request_scope.db,
            collection_name=Entity.JOBS.value,
            entity_model=Job,
            parent_collections={Entity.COMPANIES.value: company_id},
            specific_fields_to_select=["id", "created", "position_title"],
        ).data

    def _create_weekday_report_data(
        self, jobs: list[Job], applications: list[Application], day_of_week: int
    ) -> WeekdayReport:
        return WeekdayReport(
            total_num_new_applicants=len(
                [
                    application
                    for application in applications
                    if application.created.weekday() == day_of_week
                    and application.created > datetime.now() - timedelta(days=7)
                ]
            ),
            total_new_jobs=len(
                [
                    job
                    for job in jobs
                    if datetime.fromtimestamp(job.created.timestamp()).weekday()
                    == day_of_week
                    and datetime.fromtimestamp(job.created.timestamp())
                ]
            ),
        )

    def _create_weekly_report_data(
        self,
        recruiter: RecruiterDetails,
        recruiter_email: str,
        company_name: str,
        recruiter_name: str,
        jobs: list[Job],
        applications: list[Application],
    ) -> WeeklyReportData:
        return WeeklyReportData(
            user_id=recruiter.user_id,
            company_name=company_name,
            user_first_name=recruiter_name,
            user_email=recruiter_email,
            total_num_new_applicants=len(
                [
                    application
                    for application in applications
                    if application.created > datetime.now() - timedelta(days=7)
                ]
            ),
            total_num_applicants=len(applications),
            total_open_jobs=len(jobs),
            total_new_jobs=len(
                [
                    job
                    for job in jobs
                    if datetime.fromtimestamp(job.created.timestamp())
                    > datetime.utcnow() - timedelta(days=7)
                ]
            ),
            monday=self._create_weekday_report_data(jobs, applications, day_of_week=0),
            tuesday=self._create_weekday_report_data(jobs, applications, day_of_week=1),
            wednesday=self._create_weekday_report_data(
                jobs, applications, day_of_week=2
            ),
            thursday=self._create_weekday_report_data(
                jobs, applications, day_of_week=3
            ),
            friday=self._create_weekday_report_data(jobs, applications, day_of_week=4),
            saturday=self._create_weekday_report_data(
                jobs, applications, day_of_week=5
            ),
            sunday=self._create_weekday_report_data(jobs, applications, day_of_week=6),
        )

    def create_company_weekly_report(
        self, company_id: str, company_name: str
    ) -> list[WeeklyReportData]:
        recruiter_details = (
            self.recruiter_details_repository.get_all_recruiter_details_for_company(
                company_id=company_id
            )
        )
        applications = self.get_applications_for_company(company_id=company_id)
        jobs = self.get_created_jobs_for_company(company_id=company_id)
        output = []
        for recruiter in recruiter_details:
            if not recruiter.send_weekly_updates:
                continue

            # Make report
            recruiter_name, recruiter_email = self.get_recruiter_name_email(
                user_id=recruiter.user_id
            )
            output.append(
                self._create_weekly_report_data(
                    recruiter=recruiter,
                    recruiter_email=recruiter_email,
                    company_name=company_name,
                    recruiter_name=recruiter_name,
                    jobs=jobs,
                    applications=applications,
                )
            )
        return output

    def send_recruiter_report(self, report: WeeklyReportData):
        logging.info("Sending weekly report to recruiter: %s", report.user_id)
        self.mailgun.send_filled_template(
            to_address=report.user_email,
            subject="Your weekly Application Update",
            template_name="weekly_application_update.html",
            variables=report.dict(),
        )

    def create_send_all_company_reports(self, company_id: str, company_name: str):
        logging.info("Creating and sending weekly reports for company: %s", company_id)
        all_report_data = self.create_company_weekly_report(
            company_id=company_id, company_name=company_name
        )
        for report in all_report_data:
            self.send_recruiter_report(report=report)

    def run_scheduled_service(self):
        all_companies = self.company_repository.query(
            pagination=FirestorePagination(limit=None)
        ).data
        with ThreadPoolExecutor() as executor:
            for company in all_companies:
                executor.submit(
                    self.create_send_all_company_reports,
                    company_id=company.id,
                    company_name=company.name,
                )
