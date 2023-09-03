from getajob.abstractions.models import BaseDataModel

from ..jobs.models import (
    UserCreateJob,
)


class CreateJobTemplate(UserCreateJob):
    ...


class JobTemplate(BaseDataModel, CreateJobTemplate):
    ...
