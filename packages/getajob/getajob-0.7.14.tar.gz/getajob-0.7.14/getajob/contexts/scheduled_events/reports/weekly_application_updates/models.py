from pydantic import BaseModel


class WeekdayReport(BaseModel):
    total_num_new_applicants: int
    total_new_jobs: int


class WeeklyReportData(BaseModel):
    user_id: str
    company_name: str
    user_first_name: str
    user_email: str
    total_num_new_applicants: int
    total_num_applicants: int
    total_open_jobs: int
    total_new_jobs: int
    monday: WeekdayReport
    tuesday: WeekdayReport
    wednesday: WeekdayReport
    thursday: WeekdayReport
    friday: WeekdayReport
    saturday: WeekdayReport
    sunday: WeekdayReport
