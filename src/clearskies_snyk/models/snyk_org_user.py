"""Snyk Org User model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykOrgUser(Model):
    """
    Model for Snyk Organization Users.

    This model represents users within a Snyk organization.
    Note that Service Accounts are not returned by this endpoint.

    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/users/{id}

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrgUser


    def my_handler(snyk_org_user: SnykOrgUser):
        # Get a specific user in an organization
        user = snyk_org_user.where("org_id=org-id-123").find("id=user-id-456")
        print(f"User: {user.name} ({user.email})")

        # Access the parent organization
        print(f"Org: {user.org.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/users"

    """
    The unique identifier for the user.
    """
    id = String()

    """
    The ID of the organization this user belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        is_searchable=True,
    )

    """
    The parent organization this user belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The name of the user.
    """
    name = String()

    """
    The email of the user.
    """
    email = String()

    """
    The username of the user.
    """
    username = String()

    """
    Whether the user status is enabled or not.
    """
    active = Boolean()

    """
    The membership details including created_at and strategy.
    """
    membership = Json()

    """
    Whether access requests are enabled.
    """
    access_requests_enabled = Boolean()

    """
    Timestamp when the user was created.
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
    URL-friendly slug for the user.
    """
    slug = String()

    """
    ID of the group the user belongs to.
    """
    group_id = String()

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
