"""Reference to SnykTenantRole model."""


class SnykTenantRoleReference:
    """Reference to SnykTenantRole model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_tenant_role

        return snyk_tenant_role.SnykTenantRole
