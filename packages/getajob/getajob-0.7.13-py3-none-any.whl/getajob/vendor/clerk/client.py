from fastapi import HTTPException
from requests import request, Response

from getajob.config.settings import SETTINGS
from getajob.exceptions import EntityNotFound

from .models import (
    ClerkCreateUser,
    ClerkCreateCompany,
    CreateInvitation,
    CreateMember,
)


class ClerkClient:
    def __init__(self):
        self.api_key = SETTINGS.CLERK_SECRET_KEY
        self.base_url = "https://api.clerk.dev"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        payload: dict | None = None,
        files: dict | None = None,
    ) -> Response:
        url = self.base_url + endpoint
        request_payload = {"method": method, "url": url, "headers": self._headers()}
        if payload:
            request_payload["json"] = payload
        if files:
            request_payload["files"] = files
        response = request(**request_payload, timeout=10)
        if response.status_code == 404:
            raise EntityNotFound(endpoint)
        if response.status_code != 200:
            raise HTTPException(
                status_code=500, detail=f"Error: {response.status_code} {response.text}"
            )
        return response

    def get_user(self, user_id: str):
        endpoint = f"/v1/users/{user_id}"
        return self._make_request("GET", endpoint)

    def get_company(self, company_id_or_slug: str):
        endpoint = f"/v1/organizations/{company_id_or_slug}"
        return self._make_request("GET", endpoint)

    def get_company_invitations(self, company_id: str):
        endpoint = f"/v1/organizations/{company_id}/invitations/pending"
        return self._make_request("GET", endpoint)

    def get_company_recruiters(self, company_id):
        endpoint = f"/v1/organizations/{company_id}/memberships"
        return self._make_request("GET", endpoint)

    def get_companies_by_user_id(self, user_id):
        endpoint = f"/v1/users/{user_id}/organization_memberships"
        return self._make_request("GET", endpoint)

    def get_all_users(self):
        endpoint = "/v1/users"
        return self._make_request("GET", endpoint)

    def get_all_companies(self):
        endpoint = "/v1/organizations"
        return self._make_request("GET", endpoint)

    def create_user(self, user_data: ClerkCreateUser):
        endpoint = "/v1/users"
        return self._make_request("POST", endpoint, payload=user_data.dict())

    def delete_user(self, user_id: str):
        endpoint = f"/v1/users/{user_id}"
        return self._make_request("DELETE", endpoint)

    def update_user_profile_picture(
        self, user_id: str, file_bytes: bytes, file_type: str, file_name: str
    ):
        endpoint = f"/v1/users/{user_id}/profile_image"
        return self._make_request(
            "POST", endpoint, files={"file": (file_name, file_bytes, file_type)}
        )

    def create_signin_token(self, user_id: str, expires_in_seconds: int = 3600):
        endpoint = "/v1/sign_in_tokens"
        return self._make_request(
            "POST",
            endpoint,
            payload={"user_id": user_id, "expires_in_seconds": expires_in_seconds},
        )

    def revoke_signin_token(self, sign_in_token_id: str):
        endpoint = f"/v1/sign_in_tokens/{sign_in_token_id}/revoke"
        return self._make_request("POST", endpoint)

    def create_organization(self, organization_data: ClerkCreateCompany):
        endpoint = "/v1/organizations"
        return self._make_request("POST", endpoint, payload=organization_data.dict())

    def create_organization_membership(
        self, organization_id: str, membership_data: CreateMember
    ):
        endpoint = f"/v1/organizations/{organization_id}/memberships"
        return self._make_request("POST", endpoint, payload=membership_data.dict())

    def delete_an_organization(self, organization_id: str):
        endpoint = f"/v1/organizations/{organization_id}"
        return self._make_request("DELETE", endpoint)

    def update_organization_logo(
        self, organization_id: str, file_bytes: bytes, file_type: str, file_name: str
    ):
        endpoint = f"/v1/organizations/{organization_id}/logo"
        return self._make_request(
            "POST", endpoint, files={"file": (file_name, file_bytes, file_type)}
        )

    def create_organization_invitation(
        self, organization_id: str, invitation_data: CreateInvitation
    ):
        endpoint = f"/v1/organizations/{organization_id}/invitations"
        return self._make_request("POST", endpoint, payload=invitation_data.dict())
