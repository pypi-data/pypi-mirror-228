from enum import Enum
from pydantic import BaseModel, Field


class ClerkWebhookEvent(BaseModel):
    data: dict
    object: str
    type: Enum


class ClerkBaseModel(BaseModel):
    id: str
    object: str


class ClerkCompanyMemberType(str, Enum):
    admin = "admin"
    basic_member = "basic_member"


class ClerkInvitationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    revoked = "revoked"


class ClerkCompanyWebhookType(str, Enum):
    organization_created = "organization.created"
    organization_deleted = "organization.deleted"
    organization_updated = "organization.updated"


class ClerkCompanyWebhookEvent(ClerkWebhookEvent):
    type: ClerkCompanyWebhookType


class ClerkCompany(ClerkBaseModel):
    created_at: int
    created_by: str
    image_url: str | None = None
    logo_url: str | None = None
    name: str
    public_metadata: dict = {}
    slug: str | None = None
    updated_at: int | None = None


class ClerkCompanyCreated(ClerkBaseModel):
    image_url: str | None = None
    logo_url: str | None = None
    name: str | None = None
    public_metadata: dict = {}
    slug: str | None = None
    updated_at: int | None = None


class ClerkCompanyDeleted(ClerkBaseModel):
    deleted: bool


class ClerkCompanyInvitationsWebhookType(str, Enum):
    organization_invitation_created = "organizationInvitation.created"
    organization_invitation_revoked = "organizationInvitation.revoked"
    organization_invitation_accepted = "organizationInvitation.accepted"


class ClerkCompanyInvitationsWebhookEvent(ClerkWebhookEvent):
    type: ClerkCompanyInvitationsWebhookType


class ClerkCompanyInvitation(ClerkBaseModel):
    created_at: int
    email_address: str
    organization_id: str
    role: ClerkCompanyMemberType
    status: ClerkInvitationStatus
    updated_at: int


class ClerkCompanyMembershipWebhookType(str, Enum):
    organization_membership_created = "organizationMembership.created"
    organization_membership_deleted = "organizationMembership.deleted"
    organization_membership_updated = "organizationMembership.updated"


class ClerkCompanyMembershipWebhookEvent(ClerkWebhookEvent):
    type: ClerkCompanyMembershipWebhookType


class CreateClerkCompanyMember(BaseModel):
    image_url: str | None = None
    profile_image_url: str | None = None
    user_id: str


class ClerkCompanyMember(CreateClerkCompanyMember):
    id: str
    role: ClerkCompanyMemberType
    company_id: str
    user_id: str


class UpdateClerkCompanyMember(BaseModel):
    image_url: str | None = None
    profile_image_url: str | None = None
    user_id: str | None = None


class UpdateClerkCompanyMemberWithRole(UpdateClerkCompanyMember):
    role: ClerkCompanyMemberType | None = None


class ClerkCompanyMembership(ClerkBaseModel):
    created_at: int
    organization: ClerkCompanyCreated
    public_user_data: CreateClerkCompanyMember
    role: ClerkCompanyMemberType
    updated_at: int


class DeleteClerkCompanyMember(BaseModel):
    id: str


class ClerkUpdateCompanyMembership(ClerkBaseModel):
    created_at: int
    organization: ClerkCompanyCreated
    public_user_data: UpdateClerkCompanyMember
    role: ClerkCompanyMemberType
    updated_at: int


class ClerkUserWebhookType(str, Enum):
    user_created = "user.created"
    user_deleted = "user.deleted"
    user_updated = "user.updated"


class ClerkUserWebhookEvent(ClerkWebhookEvent):
    type: ClerkUserWebhookType


class ClerkUserEmailAddresses(ClerkBaseModel):
    email_address: str
    linked_to: list = Field(default_factory=list)
    verification: dict = Field(default_factory=dict)


class ClertkUserPhoneNumbers(ClerkBaseModel):
    linked_to: list
    phone_number: str
    verification: dict


class ClerkUser(ClerkBaseModel):
    created_at: int
    primary_email_address_id: str
    email_addresses: list[ClerkUserEmailAddresses]
    phone_numbers: list[ClertkUserPhoneNumbers]
    first_name: str
    last_name: str
    gender: str
    external_id: str | None = None
    birthday: str
    image_url: str | None = None


class ClerkWebhookUserUpdated(ClerkBaseModel):
    primary_email_address_id: str | None = None
    email_addresses: list[ClerkUserEmailAddresses] | None = None
    phone_numbers: list[ClertkUserPhoneNumbers] | None = None
    first_name: str | None = None
    last_name: str | None = None
    gender: str | None = None
    external_id: str | None = None
    birthday: str | None = None
    updated_at: int


class ClerkWebhookUserDeleted(ClerkBaseModel):
    deleted: bool


class ClerkCreateUser(BaseModel):
    external_id: str
    first_name: str
    last_name: str
    email_address: list[str]
    phone_number: list[str] = Field(default_factory=list)
    username: str
    password: str
    skip_password_checks: bool = False
    skip_password_requirement: bool = False
    public_metadata: dict = Field(default_factory=dict)
    private_metadata: dict = Field(default_factory=dict)
    unsafe_metadata: dict = Field(default_factory=dict)


class ClerkCreateCompany(BaseModel):
    name: str
    created_by: str


class CreateMember(BaseModel):
    user_id: str
    role: ClerkCompanyMemberType


class CreateInvitation(BaseModel):
    email_address: str
    inviter_user_id: str
    role: ClerkCompanyMemberType


class SignInToken(BaseModel):
    object: str
    id: str
    status: str
    user_id: str
    token: str
    url: str
    created_at: int
    updated_at: int
