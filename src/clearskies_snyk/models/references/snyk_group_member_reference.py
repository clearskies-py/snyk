"""Reference to SnykGroupMember model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_member import SnykGroupMember


class SnykGroupMemberReference(ModelClassReference["SnykGroupMember"]):
    """Reference to SnykGroupMember model."""

    def get_model_class(self) -> type["SnykGroupMember"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_member

        return snyk_group_member.SnykGroupMember
