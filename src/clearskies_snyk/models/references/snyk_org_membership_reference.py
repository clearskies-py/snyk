"""Reference to SnykOrgMembership model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_membership import SnykOrgMembership


class SnykOrgMembershipReference(ModelClassReference["SnykOrgMembership"]):
    """Reference to SnykOrgMembership model."""

    def get_model_class(self) -> type["SnykOrgMembership"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_membership

        return snyk_org_membership.SnykOrgMembership
