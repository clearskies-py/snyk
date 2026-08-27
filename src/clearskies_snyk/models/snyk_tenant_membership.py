"""Snyk Tenant Membership model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, Datetime, Json, Select, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_tenant_reference


class SnykTenantMembership(Model):
    """
    Model for Snyk Tenant Memberships.

    This model represents memberships in a Snyk tenant. Tenant memberships
    define the relationship between users and tenants, including their roles.

    Uses the Snyk v2 REST API endpoint: /tenants/{tenant_id}/memberships

    ```python
    import clearskies
    from clearskies_snyk.models import SnykTenantMembership


    def my_handler(snyk_tenant_membership: SnykTenantMembership):
        # Fetch all memberships for a tenant
        memberships = snyk_tenant_membership.where("tenant_id=tenant-id-123")
        for membership in memberships:
            print(f"Membership: {membership.id}")

        # Access the parent tenant
        print(f"Tenant: {membership.tenant.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(resource_type="tenant_membership", can_create=False)

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

    """
    Account type for the member.
    """
    account_type = String()

    """
    Whether the member is active.
    """
    active = Boolean()

    """
    Email of the member.
    """
    email = String()

    """
    Login method for the member.
    """
    login_method = String()

    """
    Username of the member.
    """
    username = String()

    """
    Name of the member.
    """
    name = String()

    """
    URL-friendly slug.
    """
    slug = String()

    """
    Timestamp when last updated.
    """
    updated_at = Datetime()

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
    sort_by = Select(
        allowed_values=["username", "user_display_name", "email", "login_method", "role_name"],
        is_searchable=True,
        is_temporary=True,
    )

    """
    Sort order.
    """
    sort_order = Select(allowed_values=["ASC", "DESC"], is_searchable=True, is_temporary=True)

    """
    Filter by connection type.
    """
    connection_type = String(is_searchable=True, is_temporary=True)
