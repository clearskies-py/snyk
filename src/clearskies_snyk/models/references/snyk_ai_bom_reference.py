"""Reference to SnykAiBom model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_ai_bom import SnykAiBom


class SnykAiBomReference(ModelClassReference["SnykAiBom"]):
    """Reference to SnykAiBom model."""

    def get_model_class(self) -> type["SnykAiBom"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_ai_bom

        return snyk_ai_bom.SnykAiBom
