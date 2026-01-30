"""Snyk Org Service Account model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Integer, Select, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykOrgServiceAccount(Model):
    """
    Model for Snyk Organization Service Accounts.

    This model represents service accounts at the organization level in Snyk.

    ```python
    from clearskies_snyk.models import SnykOrgServiceAccount

    # Fetch all service accounts for an organization
    accounts = SnykOrgServiceAccount().where("org_id=org-id-123")
    for account in accounts:
        print(f"Service Account: {account.name} ({account.auth_type})")

    # Access the parent organization
    print(f"Org: {account.org.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/service_accounts"

    """
    The unique identifier for the service account.
    """
    id = String()

    """
    The ID of the group this service account belongs to.
    """
    group_id = String()

    """
    The ID of the organization this service account belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        readable_parent_columns=["id", "name", "slug"],
        is_searchable=True,
    )

    """
    The parent organization this service account belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

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
