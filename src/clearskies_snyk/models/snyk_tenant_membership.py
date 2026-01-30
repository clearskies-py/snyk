"""Snyk Tenant Membership model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_tenant_reference


class SnykTenantMembership(Model):
    """
    Model for Snyk Tenant Memberships.

    This model represents memberships in a Snyk tenant. Tenant memberships
    define the relationship between users and tenants, including their roles.

    Uses the Snyk v2 REST API endpoint: /tenants/{tenant_id}/memberships

    ```python
    from clearskies_snyk.models import SnykTenantMembership

    # Fetch all memberships for a tenant
    memberships = SnykTenantMembership().where("tenant_id=tenant-id-123")
    for membership in memberships:
        print(f"Membership: {membership.id}")

    # Access the parent tenant
    print(f"Tenant: {membership.tenant.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "tenants/{tenant_id}/memberships"

    """
    The unique identifier for the membership.
    """
    id = String()

    """
    The ID of the tenant this membership belongs to.
    """
    tenant_id = BelongsToId(
        snyk_tenant_reference.SnykTenantReference,
        readable_parent_columns=["id", "name", "slug"],
        is_searchable=True,
    )

    """
    The parent tenant this membership belongs to.

    BelongsTo relationship to SnykTenant.
    """
    tenant = BelongsToModel("tenant_id")

    """
    Timestamp of when the membership was created.
    """
    created_at = Datetime()

    """
    The role relationship data.
    """
    role = Json()

    """
    The user relationship data.
    """
    user = Json()
