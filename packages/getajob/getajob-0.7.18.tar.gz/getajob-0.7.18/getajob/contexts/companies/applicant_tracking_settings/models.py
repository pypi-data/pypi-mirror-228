"""
Define the stages and data that are used across all applicant tracking for a company's given ATS
"""


from pydantic import BaseModel, Field

from getajob.abstractions.models import BaseDataModel


class SetATSConfig(BaseModel):
    available_statuses_and_order: dict[str, str] = Field(default_factory=dict)

    @classmethod
    def create_default(cls):
        default_statuses = {
            '1': "Rejected",
            '2': "Applied",
            '3': "Interviewing",
            '4': "Offered",
            '5': "Hired",
        }
        return cls(available_statuses_and_order=default_statuses)


class ATSConfig(SetATSConfig, BaseDataModel):
    ...
