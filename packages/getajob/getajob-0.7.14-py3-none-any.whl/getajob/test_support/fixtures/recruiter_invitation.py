import json

from getajob.contexts.webhooks.recruiter_invitation.repository import (
    WebhookCompanyInvitationRepository,
)
from getajob.vendor.clerk.models import (
    ClerkCompanyInvitationsWebhookEvent,
)


class RecruiterInvitationFixture:
    @staticmethod
    def create_recruiter_invitation_from_webhook(request_scope):
        with open("tests/mocks/webhooks/create_recruiter_invitation.json", "r") as f:
            data = json.load(f)
        invitation = ClerkCompanyInvitationsWebhookEvent(**data)
        repo = WebhookCompanyInvitationRepository(request_scope)
        return repo.create_invitation(invitation)
