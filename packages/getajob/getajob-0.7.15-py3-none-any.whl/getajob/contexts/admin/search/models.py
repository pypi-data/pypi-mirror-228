from datetime import datetime
from pydantic import BaseModel

from getajob.abstractions.models import Entity
from getajob.vendor.firestore.models import FirestoreOrderBy, FirestorePagination


class AdminEntitySearch(BaseModel):
    entity_type: Entity


class TimeRange(BaseModel):
    start: datetime
    end: datetime


class AdminTimeSeriesSearch(BaseModel):
    entity: Entity
    specific_fields_to_select: list[str] | None
    order_by: FirestoreOrderBy | None = None
    pagination: FirestorePagination = FirestorePagination()
    time_range: TimeRange | None = None
