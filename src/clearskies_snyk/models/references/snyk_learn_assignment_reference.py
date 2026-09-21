"""Reference to SnykLearnAssignment model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_learn_assignment import SnykLearnAssignment


class SnykLearnAssignmentReference(ModelClassReference["SnykLearnAssignment"]):
    """Reference to SnykLearnAssignment model."""

    def get_model_class(self) -> type["SnykLearnAssignment"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_learn_assignment

        return snyk_learn_assignment.SnykLearnAssignment
