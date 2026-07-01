"""Reference to SnykContainerImage model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_container_image import SnykContainerImage


class SnykContainerImageReference(ModelClassReference["SnykContainerImage"]):
    """Reference to SnykContainerImage model."""

    def get_model_class(self) -> type["SnykContainerImage"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_container_image

        return snyk_container_image.SnykContainerImage
