"""Reference to SnykOrgPolicy model."""


class SnykOrgPolicyReference:
    """Reference to SnykOrgPolicy model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_policy

        return snyk_org_policy.SnykOrgPolicy
