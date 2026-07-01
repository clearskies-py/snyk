"""Reference to SnykOrgInvite model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_invite import SnykOrgInvite


class SnykOrgInviteReference(ModelClassReference["SnykOrgInvite"]):
    """Reference to SnykOrgInvite model."""

    def get_model_class(self) -> type["SnykOrgInvite"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_invite

        return snyk_org_invite.SnykOrgInvite
