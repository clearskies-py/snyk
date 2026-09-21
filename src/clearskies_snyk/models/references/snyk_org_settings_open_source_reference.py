"""Reference to SnykOrgSettingsOpenSource model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_settings_open_source import SnykOrgSettingsOpenSource


class SnykOrgSettingsOpenSourceReference(ModelClassReference["SnykOrgSettingsOpenSource"]):
    """Reference to SnykOrgSettingsOpenSource model."""

    def get_model_class(self) -> type["SnykOrgSettingsOpenSource"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_settings_open_source

        return snyk_org_settings_open_source.SnykOrgSettingsOpenSource
