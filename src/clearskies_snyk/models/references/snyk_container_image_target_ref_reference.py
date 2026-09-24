"""Reference to SnykContainerImageTargetRef model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_container_image_target_ref import SnykContainerImageTargetRef


class SnykContainerImageTargetRefReference(ModelClassReference["SnykContainerImageTargetRef"]):
    """Reference to SnykContainerImageTargetRef model."""

    def get_model_class(self) -> type["SnykContainerImageTargetRef"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_container_image_target_ref

        return snyk_container_image_target_ref.SnykContainerImageTargetRef
