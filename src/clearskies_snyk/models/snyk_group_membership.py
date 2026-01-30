"""Snyk Group Membership model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_group_reference


class SnykGroupMembership(Model):
    """
    Model for Snyk Group Memberships.

    This model represents memberships in a Snyk group, including user and role information.

    ```python
    from clearskies_snyk.models import SnykGroupMembership

    # Fetch all memberships for a group
    memberships = SnykGroupMembership().where("group_id=group-id-123")
    for membership in memberships:
        print(f"User: {membership.name} - Role: {membership.role}")

    # Access the parent group
    print(f"Group: {membership.group_model.name}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'membership_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "membership_type",
        }
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/memberships"

    """
    The unique identifier for the membership.
    """
    id = String()

    """
    The ID of the group this membership belongs to.
    """
    group_id = BelongsToId(
        snyk_group_reference.SnykGroupReference,
        readable_parent_columns=["id", "name"],
        is_searchable=True,
    )

    """
    The parent group this membership belongs to.

    BelongsTo relationship to SnykGroup.
    Note: Named 'group_model' to avoid conflict with 'group' Json column.
    """
    group_model = BelongsToModel("group_id")

    """
    User information as JSON object.
    """
    user = Json()

    """
    Role information as JSON object.
    """
    role = Json()

    """
    Group information as JSON object.
    """
    group = Json()

    """
    The type of membership.
    """
    membership_type = String()

    """
    The ID of the user.
    """
    user_id = String()

    """
    The ID of the role.
    """
    role_id = String()

    """
    The ID of the group role.
    """
    group_role_id = String()

    """
    Whether to include group membership count in response.
    """
    include_group_membership_count = Boolean(is_searchable=True, is_temporary=True)

    """
    Metadata about the membership.
    """
    meta = Json()

    def get_membership_count(self) -> int:
        """Get membership count from metadata if available."""
        try:
            return int(self.meta.get("group_membership_count", 0))
        except (KeyError, TypeError, AttributeError, ValueError):
            return 0

    @property
    def email(self) -> str:
        """Get email from user object."""
        try:
            return str(self.user.get("email", ""))
        except (KeyError, AttributeError):
            return ""

    @property
    def name(self) -> str:
        """Get name from user object."""
        try:
            return str(self.user.get("name", ""))
        except (KeyError, AttributeError):
            return ""

    @property
    def username(self) -> str:
        """Get username from user object."""
        try:
            return str(self.user.get("username", ""))
        except (KeyError, AttributeError):
            return ""
