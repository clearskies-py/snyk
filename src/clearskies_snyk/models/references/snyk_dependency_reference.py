"""Reference to SnykDependency model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.v1.snyk_dependency import SnykDependency


class SnykDependencyReference(ModelClassReference["SnykDependency"]):
    """Reference to SnykDependency model."""

    def get_model_class(self) -> type["SnykDependency"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_dependency

        return snyk_dependency.SnykDependency
