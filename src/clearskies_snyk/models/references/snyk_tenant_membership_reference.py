"""Reference to SnykTenantMembership model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_tenant_membership import SnykTenantMembership


class SnykTenantMembershipReference(ModelClassReference["SnykTenantMembership"]):
    """Reference to SnykTenantMembership model."""

    def get_model_class(self) -> type["SnykTenantMembership"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_tenant_membership

        return snyk_tenant_membership.SnykTenantMembership
