"""Reference to SnykProjectSbom model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_project_sbom import SnykProjectSbom


class SnykProjectSbomReference(ModelClassReference["SnykProjectSbom"]):
    """Reference to SnykProjectSbom model."""

    def get_model_class(self) -> type["SnykProjectSbom"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_project_sbom

        return snyk_project_sbom.SnykProjectSbom
