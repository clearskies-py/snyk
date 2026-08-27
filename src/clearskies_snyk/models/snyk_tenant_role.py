"""Snyk Tenant Role model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_tenant_reference


class SnykTenantRole(Model):
    """
    Model for Snyk Tenant Roles.

    This model represents roles defined at the tenant level in Snyk.
    Roles control permissions and access within a tenant.

    ```python
    import clearskies
    from clearskies_snyk.models import SnykTenantRole


    def my_handler(snyk_tenant_role: SnykTenantRole):
        # Fetch all roles for a tenant
        roles = snyk_tenant_role.where("tenant_id=tenant-id-123")
        for role in roles:
            print(f"Role: {role.name} - {role.description}")

        # Access the parent tenant
        print(f"Tenant: {role.tenant.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(resource_type="tenant_role")

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "tenants/{tenant_id}/roles"

    """
    The unique identifier for the role.
    """
    id = String()

    """
    The ID of the tenant this role belongs to.
    """
    tenant_id = BelongsToId(
        snyk_tenant_reference.SnykTenantReference,
        is_searchable=True,
    )

    """
    The parent tenant this role belongs to.

    BelongsTo relationship to SnykTenant.
    """
    tenant = BelongsToModel("tenant_id")

    """
    The name of the role.
    """
    name = String()

    """
    The description of the role.
    """
    description = String()

    """
    Timestamp of when the role was created.
    """
    created = Datetime()

    """
    Timestamp of when the role was last modified.
    """
    modified = Datetime()

    """
    Permissions granted by this role.
    """
    permissions = Json()

    """
    Whether this is a custom role. Also used as search filter.
    """
    custom = Boolean(is_searchable=True)

    """
    Normalized name of the role.
    """
    normalized_name = String()

    """
    Filter roles assignable by the current user.
    """
    assignable_by_me = Boolean(is_searchable=True, is_temporary=True)

    """
    Expand permission details in the response.
    """
    expand_permissions = Boolean(is_searchable=True, is_temporary=True)

    """
    Filter roles that have users assigned.
    """
    has_users_assigned = Boolean(is_searchable=True, is_temporary=True)

    """
    Force the operation.
    """
    force = Boolean(is_searchable=True, is_temporary=True)
