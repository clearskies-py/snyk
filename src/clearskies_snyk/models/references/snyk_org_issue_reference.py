"""Reference to SnykOrgIssue model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_issue import SnykOrgIssue


class SnykOrgIssueReference(ModelClassReference["SnykOrgIssue"]):
    """Reference to SnykOrgIssue model."""

    def get_model_class(self) -> type["SnykOrgIssue"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_issue

        return snyk_org_issue.SnykOrgIssue
