from getajob.abstractions.models import PaginatedResponse, UserAndDatabaseConnection
from getajob.abstractions.repository import query_collection_group
from getajob.vendor.firestore.models import FirestoreFilters

from .models import AdminEntitySearch, AdminTimeSeriesSearch


class AdminSearchRepository:
    def __init__(self, request_scope: UserAndDatabaseConnection):
        self.db = request_scope.db

    def admin_search(self, search: AdminEntitySearch):
        return query_collection_group(
            db=self.db, collection_name=search.entity_type.value
        )

    def get_timeseries_data(self, search: AdminTimeSeriesSearch) -> PaginatedResponse:
        if search.time_range:
            filters = [
                FirestoreFilters(
                    field="created", operator=">=", value=search.time_range.start
                ),
                FirestoreFilters(
                    field="created", operator="<=", value=search.time_range.end
                ),
            ]
        else:
            filters = None
        return query_collection_group(
            db=self.db,
            collection_name=search.entity.value,
            specific_fields_to_select=search.specific_fields_to_select,
            order_by=search.order_by,
            filters=filters,
            pagination=search.pagination,
        )
