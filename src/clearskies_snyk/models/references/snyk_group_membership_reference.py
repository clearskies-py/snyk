"""Reference to SnykGroupMembership model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_membership import SnykGroupMembership


class SnykGroupMembershipReference(ModelClassReference["SnykGroupMembership"]):
    """Reference to SnykGroupMembership model."""

    def get_model_class(self) -> type["SnykGroupMembership"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_membership

        return snyk_group_membership.SnykGroupMembership
