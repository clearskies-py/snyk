"""Reference to SnykGroupPolicy model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_policy import SnykGroupPolicy


class SnykGroupPolicyReference(ModelClassReference["SnykGroupPolicy"]):
    """Reference to SnykGroupPolicy model."""

    def get_model_class(self) -> type["SnykGroupPolicy"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_policy

        return snyk_group_policy.SnykGroupPolicy
