"""Snyk Group Org Membership model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend


class SnykGroupOrgMembership(Model):
    """
    Model for Snyk Group Organization Memberships.

    This model represents organization memberships within a group.

    ```python
    import clearskies
    from clearskies_snyk.models import SnykGroupOrgMembership


    def my_handler(snyk_group_org_membership: SnykGroupOrgMembership):
        # Fetch all org memberships for a group
        memberships = snyk_group_org_membership.where("group_id=group-id-123")
        for membership in memberships:
            print(f"User: {membership.user_id} - Org: {membership.org_name}")
    ```
    """

    id_column_name: str = "user_id"

    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/org_memberships"

    """
    The ID of the user.
    """
    user_id = String(is_searchable=True)

    """
    The ID of the group.
    """
    group_id = String(is_searchable=True)

    """
    The ID of the organization.
    """
    org_id = String()

    """
    Role information as JSON object.
    """
    role = Json()

    """
    The ID of the role.
    """
    role_id = String()

    """
    The name of the organization.
    """
    org_name = String()

    """
    The name of the role.
    """
    role_name = String()

    """
    Organization information as JSON object.
    """
    org = Json()

    """
    User information as JSON object.
    """
    user = Json()

    """
    Name of the member.
    """
    name = String()

    """
    URL-friendly slug.
    """
    slug = String()

    """
    URL of the avatar.
    """
    avatar_url = String()

    """
    URL of the logo.
    """
    logo_url = String()

    """
    Timestamp when created.
    """
    created_at = Datetime()

    """
    Timestamp when last updated.
    """
    updated_at = Datetime()

    """
    Email of the member.
    """
    email = String()

    """
    Username of the member.
    """
    username = String()

    """
    Sort field.
    """
    sort_by = String(is_searchable=True, is_temporary=True)

    """
    Sort order.
    """
    sort_order = String(is_searchable=True, is_temporary=True)

    """
    Cascade membership changes.
    """
    cascade = Boolean(is_searchable=True, is_temporary=True)

    """
    Include group membership count.
    """
    include_group_membership_count = Boolean(is_searchable=True, is_temporary=True)
