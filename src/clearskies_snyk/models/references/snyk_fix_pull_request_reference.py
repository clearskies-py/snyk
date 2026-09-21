"""Reference to SnykFixPullRequest model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_fix_pull_request import SnykFixPullRequest


class SnykFixPullRequestReference(ModelClassReference["SnykFixPullRequest"]):
    """Reference to SnykFixPullRequest model."""

    def get_model_class(self) -> type["SnykFixPullRequest"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_fix_pull_request

        return snyk_fix_pull_request.SnykFixPullRequest
