"""Snyk Group Service Account model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Integer, Select, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_group_reference


class SnykGroupServiceAccount(Model):
    """
    Model for Snyk Group Service Accounts.

    This model represents service accounts at the group level in Snyk.

    ```python
    from clearskies_snyk.models import SnykGroupServiceAccount

    # Fetch all service accounts for a group
    accounts = SnykGroupServiceAccount().where("group_id=group-id-123")
    for account in accounts:
        print(f"Service Account: {account.name} ({account.auth_type})")

    # Access the parent group
    print(f"Group: {account.group.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/service_accounts"

    """
    The unique identifier for the service account.
    """
    id = String()

    """
    The ID of the group this service account belongs to.
    """
    group_id = BelongsToId(
        snyk_group_reference.SnykGroupReference,
        is_searchable=True,
    )

    """
    The parent group this service account belongs to.

    BelongsTo relationship to SnykGroup.
    """
    group = BelongsToModel("group_id")

    """
    The authentication type for the service account.
    """
    auth_type = Select(
        allowed_values=["api_key", "oauth_client_secret", "oauth_private_key_jwt"],
    )

    """
    The name of the service account.
    """
    name = String()

    """
    The ID of the role assigned to the service account.
    """
    role_id = String()

    """
    The API key for the service account (if auth_type is api_key).
    """
    api_key = String()

    """
    The client ID for OAuth authentication.
    """
    client_id = String()

    """
    The client secret for OAuth authentication.
    """
    client_secret = String()

    """
    The JWKS URL for JWT authentication.
    """
    jwks_url = String()

    """
    The level of the service account (Group or Org).
    """
    level = Select(
        allowed_values=["Group", "Org"],
    )

    """
    The TTL for access tokens in seconds.
    """
    access_token_ttl_seconds = Integer()

    """
    Timestamp of when the service account was created.
    """
    created_at = Datetime()
