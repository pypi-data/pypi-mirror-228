from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import (
    KafkaEventConfig,
    KafkaTopic,
    KafkaCompanyDetailsEnum,
)
from getajob.abstractions.models import Entity, UserAndDatabaseConnection
from getajob.vendor.firebase_storage.repository import FirebaseStorageRepository

from .models import CompanyDetails, CompanyUploadsImage, SetCompanyDetails


class CompanyDetailsRepository(SingleChildRepository[CompanyDetails]):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
        kafka: KafkaProducerRepository | None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.companies, message_type_enum=KafkaCompanyDetailsEnum
        )
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.COMPANY_DETAILS.value,
                entity_model=CompanyDetails,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
            ),
            required_parent_keys=[Entity.COMPANIES.value],
        )

    def upload_company_profile_image(
        self,
        storage: FirebaseStorageRepository,
        company_id: str,
        company_image: CompanyUploadsImage,
    ):
        remote_file_path = f"{company_id}/images/profile_image"
        image_url = storage.upload_bytes(
            company_image.file_data, company_image.file_type, remote_file_path, True
        )
        return self.set_sub_entity(
            data=SetCompanyDetails(company_main_image_url=image_url),
            parent_collections={Entity.COMPANIES.value: company_id},
        )
