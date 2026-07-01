"""Reference to SnykTenantRole model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_tenant_role import SnykTenantRole


class SnykTenantRoleReference(ModelClassReference["SnykTenantRole"]):
    """Reference to SnykTenantRole model."""

    def get_model_class(self) -> type["SnykTenantRole"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_tenant_role

        return snyk_tenant_role.SnykTenantRole
