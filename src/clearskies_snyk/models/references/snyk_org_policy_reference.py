"""Reference to SnykOrgPolicy model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_policy import SnykOrgPolicy


class SnykOrgPolicyReference(ModelClassReference["SnykOrgPolicy"]):
    """Reference to SnykOrgPolicy model."""

    def get_model_class(self) -> type["SnykOrgPolicy"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_policy

        return snyk_org_policy.SnykOrgPolicy
