"""Reference to SnykEntitlement model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.v1.snyk_entitlement import SnykEntitlement


class SnykEntitlementReference(ModelClassReference["SnykEntitlement"]):
    """Reference to SnykEntitlement model."""

    def get_model_class(self) -> type["SnykEntitlement"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_entitlement

        return snyk_entitlement.SnykEntitlement
