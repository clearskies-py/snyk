"""Reference to SnykOrg model."""


class SnykOrgReference:
    """Reference to SnykOrg model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org

        return snyk_org.SnykOrg
