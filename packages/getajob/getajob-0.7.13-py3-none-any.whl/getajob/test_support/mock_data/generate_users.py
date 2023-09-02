import time
import random
from faker import Faker

from getajob.abstractions.models import UserAndDatabaseConnection, Location
from getajob.vendor.firestore.repository import FirestoreDB
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.contexts.users.details.models import *
from getajob.static.enumerations import *
from getajob.vendor.clerk.models import (
    ClerkUser,
    ClerkUserEmailAddresses,
    ClertkUserPhoneNumbers,
)
from getajob.contexts.users.repository import UserRepository
from getajob.contexts.users.details.repository import UserDetailsRepository
from getajob.contexts.users.resumes.repository import ResumeRepository
from getajob.contexts.users.resumes.models import CreateResume


fake = Faker()


def mock_verification() -> dict:
    return {"verified": fake.boolean(), "verification_date": int(time.time())}


def mock_email() -> ClerkUserEmailAddresses:
    email = fake.email()
    return ClerkUserEmailAddresses(
        id=fake.uuid4(),
        object="email",
        email_address=email,
        linked_to=[fake.uuid4() for _ in range(random.randint(1, 3))],
        verification=mock_verification(),
    )


def mock_phone() -> ClertkUserPhoneNumbers:
    return ClertkUserPhoneNumbers(
        id=fake.uuid4(),
        object="phone",
        phone_number=fake.phone_number(),
        linked_to=[fake.uuid4() for _ in range(random.randint(1, 3))],
        verification=mock_verification(),
    )


random_profile_pics = [
    f"https://randomuser.me/api/portraits/men/{idx}.jpg" for idx in range(1, 99)
] + [f"https://randomuser.me/api/portraits/women/{idx}.jpg" for idx in range(1, 99)]


def mock_clerk_user() -> ClerkUser:
    emails = [mock_email() for _ in range(random.randint(1, 3))]
    phones = [mock_phone() for _ in range(random.randint(0, 2))]

    return ClerkUser(
        created_at=int(time.time()),
        primary_email_address_id=emails[0].email_address,
        email_addresses=emails,
        phone_numbers=phones,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        gender=random.choice(["male", "female", "other"]),
        external_id=fake.uuid4(),
        birthday=fake.date_of_birth(
            tzinfo=None, minimum_age=18, maximum_age=90
        ).isoformat(),
        image_url=random.choice(random_profile_pics),
        id=f"GENERATED_{fake.uuid4()}",
        object="user",
    )


def mock_demographic_data() -> DemographicData:
    return DemographicData(
        birth_year=random.randint(1970, 2005),
        has_disibility=fake.boolean(),
        arrest_record=fake.boolean(),
        consent_to_use_data=fake.boolean(),
    )


def mock_contact_information() -> ContactInformation:
    return ContactInformation(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        phone_number=fake.phone_number(),
        show_number_publically=fake.boolean(),
        user_location=Location(
            address_line_1=fake.street_address(),
            city=fake.city(),
            state=fake.state(),
            zipcode=fake.zipcode(),
            country="United States",
            lat=fake.latitude(),
            lon=fake.longitude(),
        ),
    )


def mock_most_recent_work() -> MostRecentWork:
    return MostRecentWork(job_title=fake.job(), company_name=fake.company())


def mock_education() -> Education:
    return Education(
        level_of_education=random.choice(list(LevelOfEducationEnum)),
        field_of_study=random.choice(list(FieldOfStudy)),
    )


def mock_skill() -> Skill:
    return Skill(
        skill=random.choice(list(SkillEnum)), experience_required=random.randint(1, 20)
    )


def mock_license() -> License:
    return License(
        license_name=random.choice(list(LicenseEnum)),
        expiration_date_month=random.randint(1, 12) if fake.boolean() else None,
        expiration_date_year=fake.year() if fake.boolean() else None,
        does_not_expire=fake.boolean(),
    )


def mock_certification() -> Certification:
    return Certification(
        certification_name=random.choice(list(CertificationEnum)),
        expiration_date_month=random.randint(1, 12) if fake.boolean() else None,
        expiration_date_year=fake.year() if fake.boolean() else None,
        does_not_expire=fake.boolean(),
    )


def mock_language() -> Langauge:
    return Langauge(
        language=random.choice(list(LanguageEnum)),
        language_proficiency=random.choice(list(LanguageProficiencyEnum)),
    )


def mock_qualifications() -> Qualifications:
    return Qualifications(
        most_recent_job=mock_most_recent_work(),
        education=[mock_education() for _ in range(random.randint(1, 3))],
        skills=[mock_skill() for _ in range(random.randint(1, 5))],
        licenses=[mock_license() for _ in range(random.randint(1, 2))]
        if fake.boolean()
        else None,
        certifications=[mock_certification() for _ in range(random.randint(1, 2))]
        if fake.boolean()
        else None,
        language_proficiencies=[mock_language() for _ in range(random.randint(1, 3))],
    )


def mock_job_preferences() -> JobPreferences:
    return JobPreferences(
        desired_job_title=fake.job(),
        desired_job_types=[
            random.choice(list(JobTypeEnum)) for _ in range(random.randint(1, 3))
        ],
        desired_pay=DesiredPay(
            minimum_pay=random.randint(10, 150), pay_period=PayEnum.HOURLY
        ),
        willing_to_relocate=fake.boolean(),
        desired_work_settings=[
            random.choice(list(WorkSettingEnum)) for _ in range(random.randint(0, 2))
        ],
        desired_industries=[
            random.choice(list(IndustryEnum)) for _ in range(random.randint(1, 3))
        ],
        ready_to_start_immediately=fake.boolean(),
    )


def mock_set_user_details() -> SetUserDetails:
    return SetUserDetails(
        qualifications=mock_qualifications(),
        contact_information=mock_contact_information(),
        demographics=mock_demographic_data(),
        job_preferences=mock_job_preferences(),
    )


def generate_users_details_and_resumes(num_users: int):
    db = FirestoreDB()
    kafka_repo = KafkaProducerRepository()
    user_repo = UserRepository(
        request_scope=UserAndDatabaseConnection(initiating_user_id="system", db=db),
        kafka=kafka_repo,
    )
    user_details_repo = UserDetailsRepository(
        request_scope=UserAndDatabaseConnection(initiating_user_id="system", db=db),
        kafka=kafka_repo,
    )
    user_resume_repo = ResumeRepository(
        request_scope=UserAndDatabaseConnection(initiating_user_id="system", db=db),
    )
    for _ in range(num_users):
        generated_user = mock_clerk_user()
        created_user = user_repo.create(generated_user, provided_id=generated_user.id)
        user_details_repo.create(
            data=SetUserDetails(),
            parent_collections={"users": created_user.id},
            provided_id="user_details",
        )
        time.sleep(1)
        user_details_repo.set_sub_entity(
            data=mock_set_user_details(), parent_collections={"users": created_user.id}
        )
        user_resume_repo.create(
            data=CreateResume(remote_file_path="/nice/file", resume_url=fake.url()),
            parent_collections={"users": created_user.id},
        )
