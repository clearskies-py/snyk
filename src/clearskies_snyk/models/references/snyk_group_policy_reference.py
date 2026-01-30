"""Reference to SnykGroupPolicy model."""


class SnykGroupPolicyReference:
    """Reference to SnykGroupPolicy model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_policy

        return snyk_group_policy.SnykGroupPolicy
