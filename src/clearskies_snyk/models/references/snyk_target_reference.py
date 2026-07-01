"""Reference to SnykTarget model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_target import SnykTarget


class SnykTargetReference(ModelClassReference["SnykTarget"]):
    """Reference to SnykTarget model."""

    def get_model_class(self) -> type["SnykTarget"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_target

        return snyk_target.SnykTarget
