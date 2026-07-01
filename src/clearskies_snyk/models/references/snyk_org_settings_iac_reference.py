"""Reference to SnykOrgSettingsIac model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_settings_iac import SnykOrgSettingsIac


class SnykOrgSettingsIacReference(ModelClassReference["SnykOrgSettingsIac"]):
    """Reference to SnykOrgSettingsIac model."""

    def get_model_class(self) -> type["SnykOrgSettingsIac"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_settings_iac

        return snyk_org_settings_iac.SnykOrgSettingsIac
