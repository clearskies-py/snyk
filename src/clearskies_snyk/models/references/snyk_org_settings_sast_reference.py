"""Reference to SnykOrgSettingsSast model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_settings_sast import SnykOrgSettingsSast


class SnykOrgSettingsSastReference(ModelClassReference["SnykOrgSettingsSast"]):
    """Reference to SnykOrgSettingsSast model."""

    def get_model_class(self) -> type["SnykOrgSettingsSast"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_settings_sast

        return snyk_org_settings_sast.SnykOrgSettingsSast
