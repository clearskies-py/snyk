"""Snyk Org Member model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Datetime, Email, Json, String

from clearskies_snyk.backends import SnykBackend


class SnykOrgMember(Model):
    """
    Model for Snyk Organization Members.

    This model represents members of a Snyk organization.

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrgMember


    def my_handler(snyk_org_member: SnykOrgMember):
        # Fetch all members for an organization
        members = snyk_org_member.where("org_id=org-id-123")
        for member in members:
            print(f"Member: {member.name} ({member.email})")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(resource_type="member")

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/memberships"

    """
    The unique identifier for the member.
    """
    id = String()

    """
    The ID of the organization this member belongs to.
    """
    org_id = String(is_searchable=True)

    """
    The name of the member.
    """
    name = String()

    """
    The username of the member.
    """
    username = String()

    """
    The email of the member.
    """
    email = Email()

    """
    The role of the member in the organization.
    """
    role = String()

    """
    Organizations the member belongs to.
    """
    orgs = Json()

    """
    Whether access requests are enabled.
    """
    access_requests_enabled = Boolean()

    """
    Timestamp when the membership was created.
    """
    created_at = Datetime()

    """
    Timestamp when last updated.
    """
    updated_at = Datetime()

    """
    Whether this is a personal org.
    """
    is_personal = Boolean()

    """
    URL-friendly slug.
    """
    slug = String()

    """
    Filter by user ID.
    """
    user_id = String(is_searchable=True, is_temporary=True)

    """
    Filter by role name.
    """
    role_name = String(is_searchable=True, is_temporary=True)

    """
    Sort field.
    """
    sort_by = String(is_searchable=True, is_temporary=True)

    """
    Sort order.
    """
    sort_order = String(is_searchable=True, is_temporary=True)

    """
    Expand related resources.
    """
    expand = String(is_searchable=True, is_temporary=True)

    """
    Filter by group ID.
    """
    group_id = String(is_searchable=True, is_temporary=True)
