"""Reference to SnykGroupIssue model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_issue import SnykGroupIssue


class SnykGroupIssueReference(ModelClassReference["SnykGroupIssue"]):
    """Reference to SnykGroupIssue model."""

    def get_model_class(self) -> type["SnykGroupIssue"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_issue

        return snyk_group_issue.SnykGroupIssue
