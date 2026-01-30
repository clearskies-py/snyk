"""Reference to SnykOrgMembership model."""


class SnykOrgMembershipReference:
    """Reference to SnykOrgMembership model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_membership

        return snyk_org_membership.SnykOrgMembership
