"""Reference to SnykProjectIgnore model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_project_ignore import SnykProjectIgnore


class SnykProjectIgnoreReference(ModelClassReference["SnykProjectIgnore"]):
    """Reference to SnykProjectIgnore model."""

    def get_model_class(self) -> type["SnykProjectIgnore"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_project_ignore

        return snyk_project_ignore.SnykProjectIgnore
