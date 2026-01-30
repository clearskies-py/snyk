"""Reference to SnykOrgIssue model."""


class SnykOrgIssueReference:
    """Reference to SnykOrgIssue model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_issue

        return snyk_org_issue.SnykOrgIssue
