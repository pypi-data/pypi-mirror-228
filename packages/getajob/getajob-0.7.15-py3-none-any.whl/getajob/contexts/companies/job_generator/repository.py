import json

from getajob.vendor.openai.repository import OpenAIRepository
from getajob.contexts.companies.jobs.models import UserCreateJob, JobSkill, ScheduleType


class JobGeneratorRepository:
    def __init__(self):
        self.openai = OpenAIRepository()

    def generate_job_from_description(self, description: str) -> UserCreateJob:
        job_keys = [
            "position_title",
            "description",
            "experience_required",
            "required_job_skill",
            "location_type",
            "is_full_time",
        ]
        response = self.openai.text_prompt(
            prompt=f"Given the following job description, \
            return these keys in JSON format. Keys: {job_keys}, description: {description}",
        )
        response_as_dict = json.loads(response)
        return UserCreateJob(
            position_title=response_as_dict["position_title"],
            description=response_as_dict["description"],
            experience_required=response_as_dict["experience_required"],
            required_job_skills=[
                JobSkill(
                    skill_name=response_as_dict["required_job_skill"], must_have=True
                )
            ],
            location_type=response_as_dict["location_type"],
            schedule=ScheduleType.FULL_TIME
            if response_as_dict["is_full_time"]
            else ScheduleType.PART_TIME,
        )
