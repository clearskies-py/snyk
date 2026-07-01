"""Reference to SnykIntegration model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.v1.snyk_integration import SnykIntegration


class SnykIntegrationReference(ModelClassReference["SnykIntegration"]):
    """Reference to SnykIntegration model."""

    def get_model_class(self) -> type["SnykIntegration"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_integration

        return snyk_integration.SnykIntegration
