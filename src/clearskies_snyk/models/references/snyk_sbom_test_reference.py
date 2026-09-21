"""Reference to SnykSbomTest model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_sbom_test import SnykSbomTest


class SnykSbomTestReference(ModelClassReference["SnykSbomTest"]):
    """Reference to SnykSbomTest model."""

    def get_model_class(self) -> type["SnykSbomTest"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_sbom_test

        return snyk_sbom_test.SnykSbomTest
