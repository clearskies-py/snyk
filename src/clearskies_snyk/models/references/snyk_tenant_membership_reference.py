"""Reference to SnykTenantMembership model."""


class SnykTenantMembershipReference:
    """Reference to SnykTenantMembership model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_tenant_membership

        return snyk_tenant_membership.SnykTenantMembership
