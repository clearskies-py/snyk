"""Reference to SnykTenant model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_tenant import SnykTenant


class SnykTenantReference(ModelClassReference["SnykTenant"]):
    """Reference to SnykTenant model."""

    def get_model_class(self) -> type["SnykTenant"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_tenant

        return snyk_tenant.SnykTenant
