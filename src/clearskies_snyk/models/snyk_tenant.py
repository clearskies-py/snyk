"""Snyk Tenant model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Datetime, HasMany, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_tenant_membership_reference, snyk_tenant_role_reference


class SnykTenant(Model):
    """
    Model for Snyk Tenants.

    This model represents tenants in Snyk. Tenants are the top-level container
    for organizations and groups in Snyk.

    Uses the Snyk v2 REST API endpoint: /tenants

    ```python
    import clearskies
    from clearskies_snyk.models import SnykTenant


    def my_handler(snyk_tenant: SnykTenant):
        # Fetch all tenants
        tenants = snyk_tenant
        for tenant in tenants:
            print(f"Tenant: {tenant.name} ({tenant.slug})")

        # Find a specific tenant by ID
        tenant = tenants.find("id=tenant-id-123")
        print(tenant.name)

        # Access related memberships
        for membership in tenant.memberships:
            print(f"  Membership: {membership.id}")

        # Access related roles
        for role in tenant.roles:
            print(f"  Role: {role.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "tenants"

    """
    The unique identifier for the tenant.
    """
    id = String()

    """
    The human-readable name of the tenant.
    """
    name = String()

    """
    The URL-friendly slug for the tenant.
    """
    slug = String()

    """
    Timestamp of when the tenant was created.
    """
    created_at = Datetime()

    """
    Timestamp of when the tenant was last updated.
    """
    updated_at = Datetime()

    """
    Tenant memberships.

    HasMany relationship to SnykTenantMembership.
    """
    memberships = HasMany(
        snyk_tenant_membership_reference.SnykTenantMembershipReference,
        foreign_column_name="tenant_id",
    )

    """
    Tenant roles.

    HasMany relationship to SnykTenantRole.
    """
    roles = HasMany(
        snyk_tenant_role_reference.SnykTenantRoleReference,
        foreign_column_name="tenant_id",
    )
