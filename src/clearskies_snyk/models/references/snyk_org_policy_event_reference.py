"""Reference to SnykOrgPolicyEvent model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_policy_event import SnykOrgPolicyEvent


class SnykOrgPolicyEventReference(ModelClassReference["SnykOrgPolicyEvent"]):
    """Reference to SnykOrgPolicyEvent model."""

    def get_model_class(self) -> type["SnykOrgPolicyEvent"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_policy_event

        return snyk_org_policy_event.SnykOrgPolicyEvent
