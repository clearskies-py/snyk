"""Snyk Group SSO Connection User model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Datetime, Json, Select, String

from clearskies_snyk.backends import SnykBackend


class SnykGroupSsoConnectionUser(Model):
    """
    Model for Snyk Group SSO Connection Users.

    This model represents users associated with an SSO connection at the group level.
    Uses the Snyk v2 REST API endpoint: /groups/{group_id}/sso_connections/{sso_id}/users

    ```python
    from clearskies_snyk.models import SnykGroupSsoConnectionUser

    # List users for an SSO connection
    users = SnykGroupSsoConnectionUser().where("group_id=group-id-123&sso_id=sso-id-456")
    for user in users:
        print(f"User: {user.name} ({user.email})")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'user_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "user_type",
        },
        can_create=False,
        can_update=False,
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/sso_connections/{sso_id}/users"

    """
    The unique identifier for the user.
    """
    id = String()

    """
    The ID of the group this user belongs to.
    """
    group_id = String(is_searchable=True)

    """
    The ID of the SSO connection this user is associated with.
    """
    sso_id = String(is_searchable=True)

    """
    The type of resource (user).
    """
    user_type = String()

    """
    The name of the user.
    """
    name = String()

    """
    The username of the user.
    """
    username = String()

    """
    The email of the user.
    """
    email = String()

    """
    Whether the user status is enabled or not.
    """
    active = Boolean()

    """
    Membership information.
    """
    membership = Json()

    """
    The date the membership was established.
    """
    membership_created_at = Datetime()

    """
    Whether the membership is direct or indirect.
    """
    membership_strategy = Select(allowed_values=["direct", "indirect"])
