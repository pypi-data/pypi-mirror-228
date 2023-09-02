import faker
import time
import random

from getajob.abstractions.models import UserAndDatabaseConnection, Location
from getajob.vendor.firestore.repository import FirestoreDB
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.contexts.companies.models import Company
from getajob.contexts.companies.jobs.models import *
from getajob.contexts.companies.repository import CompanyRepository
from getajob.contexts.companies.jobs.repository import JobsRepository


fake = faker.Faker()


def mock_clerk_company() -> Company:
    company_name = fake.company()
    slugified_name = fake.slug(company_name)

    return Company(
        created_at=int(time.time() * 1000),  # Current time in milliseconds
        created_by=fake.uuid4(),  # Random UUID string
        image_url=fake.image_url() if fake.boolean() else None,
        logo_url=fake.image_url() if fake.boolean() else None,
        name=company_name,
        public_metadata={},  # You can adjust this as needed
        slug=slugified_name,
        updated_at=int(time.time() * 1000),
        id=f"GENERATED_{fake.uuid4()}",
        object="company",
    )


def mock_position_category() -> PositionCategory:
    return PositionCategory(
        category=fake.job(), subcategories=[fake.job() for _ in range(5)]
    )


def mock_pay() -> Pay:
    return Pay(
        pay_min=random.randint(7, 50),
        pay_max=random.randint(50, 1500),
        pay_type=PayType.HOURLY,
        includes_bonus=fake.boolean(),
        includes_equity=fake.boolean(),
        includes_commission=fake.boolean(),
        includes_tips=fake.boolean(),
    )


def mock_create_job(company_id: str) -> CreateJob:
    return CreateJob(
        position_title=fake.job(),
        description=fake.text(),
        position_category=mock_position_category(),
        schedule=random.choice(list(ScheduleType)),
        experience_required=random.choice(list(ExperienceLevel)),
        location_type=random.choice(list(JobLocationType)),
        num_candidates_required=random.randint(1, 10),
        ongoing_recruitment=fake.boolean(),
        on_job_training_offered=fake.boolean(),
        weekly_day_range=[random.choice(list(WeeklyScheduleType))],
        shift_type=[random.choice(list(ShiftType))],
        pay=mock_pay(),
        background_check_required=fake.boolean(),
        drug_test_required=fake.boolean(),
        felons_accepted=fake.boolean(),
        disability_accepted=fake.boolean(),
        ideal_days_to_hire=random.randint(1, 10),
        job_associated_company_description=fake.text(),
        location=Location(
            address_line_1=fake.street_address(),
            city=fake.city(),
            state=fake.state(),
            zipcode=fake.zipcode(),
            country="United States",
            lat=fake.latitude(),
            lon=fake.longitude(),
        ),
        company_id=company_id,
        company_name="Great Company",
    )


def generate_companies_and_jobs(num_companies: int, num_jobs_per_company: int):
    db = FirestoreDB()
    kafka_repo = KafkaProducerRepository()
    request_scope = UserAndDatabaseConnection(initiating_user_id="system", db=db)
    company_repo = CompanyRepository(request_scope=request_scope, kafka=kafka_repo)
    jobs_repo = JobsRepository(
        request_scope=request_scope, kafka=kafka_repo, algolia_jobs=None
    )

    for _ in range(num_companies):
        company = mock_clerk_company()
        company_repo.create(data=company, provided_id=company.id)

        for __ in range(num_jobs_per_company):
            job = mock_create_job(company.id)
            jobs_repo.create_job(job=job, company_id=company.id)
