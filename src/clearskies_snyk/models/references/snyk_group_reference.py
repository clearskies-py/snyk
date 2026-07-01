"""Reference to SnykGroup model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group import SnykGroup


class SnykGroupReference(ModelClassReference["SnykGroup"]):
    """Reference to SnykGroup model."""

    def get_model_class(self) -> type["SnykGroup"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group

        return snyk_group.SnykGroup
