"""Snyk Org User model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykOrgUser(Model):
    """
    Model for Snyk Organization Users.

    This model represents users within a Snyk organization.
    Note that Service Accounts are not returned by this endpoint.

    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/users/{id}

    ```python
    from clearskies_snyk.models import SnykOrgUser

    # Get a specific user in an organization
    user = SnykOrgUser().where("org_id=org-id-123").find("id=user-id-456")
    print(f"User: {user.name} ({user.email})")

    # Access the parent organization
    print(f"Org: {user.org.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

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
        readable_parent_columns=["id", "name", "slug"],
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
