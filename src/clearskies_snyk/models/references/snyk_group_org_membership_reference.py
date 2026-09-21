"""Reference to SnykGroupOrgMembership model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_org_membership import SnykGroupOrgMembership


class SnykGroupOrgMembershipReference(ModelClassReference["SnykGroupOrgMembership"]):
    """Reference to SnykGroupOrgMembership model."""

    def get_model_class(self) -> type["SnykGroupOrgMembership"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_org_membership

        return snyk_group_org_membership.SnykGroupOrgMembership
