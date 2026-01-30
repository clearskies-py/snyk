"""Reference to SnykGroupIssue model."""


class SnykGroupIssueReference:
    """Reference to SnykGroupIssue model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_issue

        return snyk_group_issue.SnykGroupIssue
