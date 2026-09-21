"""Reference to SnykOrgUser model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_user import SnykOrgUser


class SnykOrgUserReference(ModelClassReference["SnykOrgUser"]):
    """Reference to SnykOrgUser model."""

    def get_model_class(self) -> type["SnykOrgUser"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_user

        return snyk_org_user.SnykOrgUser
