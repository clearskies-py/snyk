"""Reference to SnykGroupSettingsIac model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_settings_iac import SnykGroupSettingsIac


class SnykGroupSettingsIacReference(ModelClassReference["SnykGroupSettingsIac"]):
    """Reference to SnykGroupSettingsIac model."""

    def get_model_class(self) -> type["SnykGroupSettingsIac"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_settings_iac

        return snyk_group_settings_iac.SnykGroupSettingsIac
