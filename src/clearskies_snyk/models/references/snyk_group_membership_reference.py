"""Reference to SnykGroupMembership model."""


class SnykGroupMembershipReference:
    """Reference to SnykGroupMembership model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_membership

        return snyk_group_membership.SnykGroupMembership
