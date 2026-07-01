"""Reference to SnykGroupSettings model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.v1.snyk_group_settings import SnykGroupSettings


class SnykGroupSettingsReference(ModelClassReference["SnykGroupSettings"]):
    """Reference to SnykGroupSettings model."""

    def get_model_class(self) -> type["SnykGroupSettings"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_group_settings

        return snyk_group_settings.SnykGroupSettings
