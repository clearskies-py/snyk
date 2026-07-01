"""Reference to SnykGroupTag model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.v1.snyk_group_tag import SnykGroupTag


class SnykGroupTagReference(ModelClassReference["SnykGroupTag"]):
    """Reference to SnykGroupTag model."""

    def get_model_class(self) -> type["SnykGroupTag"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_group_tag

        return snyk_group_tag.SnykGroupTag
