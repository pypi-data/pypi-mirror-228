import typing as t

from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel, Location
from getajob.static.enumerations import (
    PayEnum,
    WorkSettingEnum,
    IndustryEnum,
    JobTypeEnum,
    SkillEnum,
    LanguageEnum,
)

from ..enumerations import (
    RaceEnum,
    GenderEnum,
    LevelOfEducationEnum,
    FieldOfStudy,
    LicenseEnum,
    CertificationEnum,
    LanguageProficiencyEnum,
)


class DemographicData(BaseModel):
    birth_year: int | None = None
    race: RaceEnum | None = None
    gender: GenderEnum | None = None
    has_disibility: bool | None = None
    arrest_record: bool | None = None
    consent_to_use_data: bool | None = None


class ContactInformation(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    show_number_publically: bool = False
    user_location: Location | None = None


class JobSchedule(BaseModel):
    # TASK enums e'rywhere baby
    days: t.List[str]
    shifts: t.List[str]
    schedules: t.List[str]


class DesiredPay(BaseModel):
    minimum_pay: int
    pay_period: PayEnum


class JobPreferences(BaseModel):
    desired_job_title: str | None = None
    desired_job_types: list[JobTypeEnum] | None = None
    desired_schedule: list[JobSchedule] | None = None
    desired_pay: DesiredPay | None = None
    willing_to_relocate: bool | None = None
    desired_work_settings: list[WorkSettingEnum] | None = None
    desired_industries: list[IndustryEnum] | None = None
    ready_to_start_immediately: bool | None = None


class MostRecentWork(BaseModel):
    job_title: str
    company_name: str


class Education(BaseModel):
    level_of_education: LevelOfEducationEnum
    field_of_study: FieldOfStudy


class Skill(BaseModel):
    skill: SkillEnum
    experience_required: int


class License(BaseModel):
    license_name: LicenseEnum
    expiration_date_month: int | None = None
    expiration_date_year: str | None = None
    does_not_expire: bool


class Certification(BaseModel):
    certification_name: CertificationEnum
    expiration_date_month: int | None = None
    expiration_date_year: str | None = None
    does_not_expire: bool


class Langauge(BaseModel):
    language: LanguageEnum
    language_proficiency: LanguageProficiencyEnum


class Qualifications(BaseModel):
    most_recent_job: MostRecentWork | None = None
    education: t.List[Education] | None = None
    skills: t.List[Skill] | None = None
    licenses: t.List[License] | None = None
    certifications: t.List[Certification] | None = None
    language_proficiencies: t.List[Langauge] | None = None

    def get_qualifications_score(self):
        """Returns a 0-100 score based on the details provided"""
        weights = {
            "most_recent_job": 40,
            "education": 25,
            "skills": 20,
            "licenses": 5,
            "certifications": 5,
            "language_proficiencies": 5,
        }

        score = 0
        for attr, weight in weights.items():
            if getattr(self, attr):
                score += weight

        return score


class SetUserDetails(BaseModel):
    qualifications: Qualifications | None = None
    contact_information: ContactInformation | None = None
    demographics: DemographicData | None = None
    job_preferences: JobPreferences | None = None

    candidate_score: float | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.qualifications:
            self.candidate_score = self.qualifications.get_qualifications_score()
        else:
            self.candidate_score = 0


class UserDetails(SetUserDetails, BaseDataModel):
    ...
