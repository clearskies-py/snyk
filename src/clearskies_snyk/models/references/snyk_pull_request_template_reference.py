"""Reference to SnykPullRequestTemplate model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_pull_request_template import SnykPullRequestTemplate


class SnykPullRequestTemplateReference(ModelClassReference["SnykPullRequestTemplate"]):
    """Reference to SnykPullRequestTemplate model."""

    def get_model_class(self) -> type["SnykPullRequestTemplate"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_pull_request_template

        return snyk_pull_request_template.SnykPullRequestTemplate
