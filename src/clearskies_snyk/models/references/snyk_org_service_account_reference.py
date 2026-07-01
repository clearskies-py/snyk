"""Reference to SnykOrgServiceAccount model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_service_account import SnykOrgServiceAccount


class SnykOrgServiceAccountReference(ModelClassReference["SnykOrgServiceAccount"]):
    """Reference to SnykOrgServiceAccount model."""

    def get_model_class(self) -> type["SnykOrgServiceAccount"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_service_account

        return snyk_org_service_account.SnykOrgServiceAccount
