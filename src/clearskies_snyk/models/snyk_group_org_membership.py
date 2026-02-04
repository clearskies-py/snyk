"""Snyk Group Org Membership model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykBackend


class SnykGroupOrgMembership(Model):
    """
    Model for Snyk Group Organization Memberships.

    This model represents organization memberships within a group.

    ```python
    from clearskies_snyk.models import SnykGroupOrgMembership

    # Fetch all org memberships for a group
    memberships = SnykGroupOrgMembership().where("group_id=group-id-123")
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
