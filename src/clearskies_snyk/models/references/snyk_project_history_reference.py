"""Reference to SnykProjectHistory model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_project_history import SnykProjectHistory


class SnykProjectHistoryReference(ModelClassReference["SnykProjectHistory"]):
    """Reference to SnykProjectHistory model."""

    def get_model_class(self) -> type["SnykProjectHistory"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_project_history

        return snyk_project_history.SnykProjectHistory
