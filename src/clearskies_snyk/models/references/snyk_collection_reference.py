"""Reference to SnykCollection model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_collection import SnykCollection


class SnykCollectionReference(ModelClassReference["SnykCollection"]):
    """Reference to SnykCollection model."""

    def get_model_class(self) -> type["SnykCollection"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_collection

        return snyk_collection.SnykCollection
