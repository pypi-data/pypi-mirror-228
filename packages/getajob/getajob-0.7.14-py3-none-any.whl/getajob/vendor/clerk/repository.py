import typing
from requests import Response
from pydantic import BaseModel

from .client import ClerkClient
from .client_factory import ClerkClientFactory
from .models import (
    ClerkCreateUser,
    ClerkCreateCompany,
    CreateInvitation,
    CreateMember,
    SignInToken,
    ClerkCompany,
    ClerkUser,
    ClerkCompanyInvitation,
    ClerkCompanyMembership,
)


class ClerkAPIRepository:
    def __init__(self, client: ClerkClient = ClerkClientFactory.get_client()):  # type: ignore
        self.client = client

    def _format_response_to_model(
        self, response: Response, model: typing.Type[BaseModel] | None
    ):
        """
        Some clerk models return a 'data' key and others don't. This method
        formats the response to a pydantic model for both cases
        """
        response_json = response.json()
        if "data" in response_json:
            response_json = response_json["data"]
        if not model:
            return response_json
        if isinstance(response_json, list):
            return [model(**item) for item in response_json]
        return model(**response_json)

    def get_user(self, user_id: str):
        user = self.client.get_user(user_id)
        return self._format_response_to_model(user, ClerkUser)

    def get_company(self, company_id: str):
        company = self.client.get_company(company_id)
        return self._format_response_to_model(company, ClerkCompany)

    def get_company_invitations(self, company_id: str):
        invitations = self.client.get_company_invitations(company_id)
        return self._format_response_to_model(invitations, ClerkCompanyInvitation)

    def get_company_recruiters(self, company_id):
        recruiters = self.client.get_company_recruiters(company_id)
        return self._format_response_to_model(recruiters, ClerkCompanyMembership)

    def get_companies_by_user_id(self, user_id) -> typing.List[ClerkCompanyMembership]:
        companies = self.client.get_companies_by_user_id(user_id)
        return self._format_response_to_model(companies, ClerkCompanyMembership)  # type: ignore

    def get_all_users(self):
        users = self.client.get_all_users()
        return self._format_response_to_model(users, ClerkUser)

    def get_all_companies(self):
        companies = self.client.get_all_companies()
        return self._format_response_to_model(companies, ClerkCompany)

    def create_user(self, user_data: ClerkCreateUser) -> ClerkUser:
        user = self.client.create_user(user_data)
        return self._format_response_to_model(user, ClerkUser)  # type: ignore

    def delete_user(self, user_id: str) -> bool:
        resp = self.client.delete_user(user_id)
        return resp.json()["deleted"]

    def create_signin_token(self, user_id: str) -> SignInToken:
        token = self.client.create_signin_token(user_id)
        return self._format_response_to_model(token, SignInToken)  # type: ignore

    def revoke_signing_token(self, token_id: str) -> bool:
        resp = self.client.revoke_signin_token(token_id)
        return resp.status_code == 200

    def create_organization(self, company_data: ClerkCreateCompany):
        company = self.client.create_organization(company_data)
        return self._format_response_to_model(company, ClerkCompany)

    def create_organization_membership(
        self, organization_id: str, member_data: CreateMember
    ):
        member = self.client.create_organization_membership(
            organization_id, member_data
        )
        return self._format_response_to_model(member, ClerkCompanyMembership)

    def create_organization_invitation(
        self, organization_id: str, invitation_data: CreateInvitation
    ):
        invitation = self.client.create_organization_invitation(
            organization_id, invitation_data
        )
        return self._format_response_to_model(invitation, ClerkCompanyInvitation)

    def delete_an_organization(self, organization_id: str) -> bool:
        resp = self.client.delete_an_organization(organization_id)
        return resp.json()["deleted"]

    def update_user_profile_picture(
        self, user_id: str, file_bytes: bytes, file_type: str, file_name: str
    ) -> bool:
        resp = self.client.update_user_profile_picture(
            user_id, file_bytes, file_type, file_name
        )
        return resp.status_code == 200

    def update_organization_logo(
        self, company_id: str, file_bytes: bytes, file_type: str, file_name: str
    ) -> bool:
        resp = self.client.update_organization_logo(
            company_id, file_bytes, file_type, file_name
        )
        return resp.status_code == 200
