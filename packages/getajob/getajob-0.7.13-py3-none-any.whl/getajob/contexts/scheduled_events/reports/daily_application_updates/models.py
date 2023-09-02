from datetime import datetime
from pydantic import BaseModel


class DailyReportBreakdown(BaseModel):
    job_id: str
    job_name: str
    job_created: datetime
    num_new_applicants: int
    num_total_applicants: int


class DailyReportData(BaseModel):
    user_id: str
    company_name: str
    user_first_name: str
    user_email: str
    total_num_new_applicants: int
    total_num_applicants: int
    total_open_jobs: int
    total_new_jobs: int
    breakdown: dict[str, DailyReportBreakdown]  # Job id -> DailyReportBreakdown


# Save for later


class WeekdayReport(BaseModel):
    num_new_applicants: int
    num_viewed_applicants: int

    # Could also add a split of where they are in the process


class WeeklyReportData(BaseModel):
    monday: WeekdayReport
    tuesday: WeekdayReport
    wednesday: WeekdayReport
    thursday: WeekdayReport
    friday: WeekdayReport
