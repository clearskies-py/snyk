"""Snyk Org Invite model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykOrgInvite(Model):
    """
    Model for Snyk Organization Invitations.

    This model represents pending user invitations to a Snyk organization.
    Invitations can be created, listed, and cancelled.

    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/invites

    ```python
    from clearskies_snyk.models import SnykOrgInvite

    # Fetch all invites for an organization
    invites = SnykOrgInvite().where("org_id=org-id-123")
    for invite in invites:
        print(f"Invite: {invite.email} ({invite.role})")

    # Access the parent organization
    print(f"Org: {invite.org.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_update=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/invites"

    """
    The unique identifier for the invitation.
    """
    id = String()

    """
    The ID of the organization this invitation belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        readable_parent_columns=["id", "name", "slug"],
        is_searchable=True,
    )

    """
    The parent organization this invitation belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The email address of the invitee.
    """
    email = String()

    """
    The role assigned to the invitee on acceptance.
    """
    role = String()

    """
    The active status of the invitation.
    is_active of true indicates that the invitation is still waiting to be accepted.
    Invitations are considered inactive when accepted or revoked.
    """
    is_active = Boolean()

    """
    The organization relationship data.
    """
    relationships = Json()
