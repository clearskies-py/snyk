"""Snyk Group Member model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Datetime, Email, Json, String

from clearskies_snyk.backends import SnykBackend


class SnykGroupMember(Model):
    """
    Model for Snyk Group Members.

    This model represents members of a Snyk group.

    ```python
    import clearskies
    from clearskies_snyk.models import SnykGroupMember


    def my_handler(snyk_group_member: SnykGroupMember):
        # Fetch all members for a group
        members = snyk_group_member.where("group_id=group-id-123")
        for member in members:
            print(f"Member: {member.name} ({member.email})")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(resource_type="member")

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/memberships"

    """
    The unique identifier for the member.
    """
    id = String()

    """
    The ID of the group this member belongs to.
    """
    group_id = String(is_searchable=True)

    """
    The ID of the organization this member belongs to.
    """
    org_id = String()

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
    The role of the member in the group.
    """
    group_role = String()

    """
    Organizations the member belongs to.
    """
    orgs = Json()

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
    Timestamp when the membership was created.
    """
    created_at = Datetime()

    """
    Timestamp when the membership was last updated.
    """
    updated_at = Datetime()

    """
    Filter by user ID.
    """
    user_id = String(is_searchable=True, is_temporary=True)

    """
    Filter by organization name.
    """
    org_name = String(is_searchable=True, is_temporary=True)

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
    Cascade membership changes.
    """
    cascade = Boolean(is_searchable=True, is_temporary=True)

    """
    Include group membership count.
    """
    include_group_membership_count = Boolean(is_searchable=True, is_temporary=True)
