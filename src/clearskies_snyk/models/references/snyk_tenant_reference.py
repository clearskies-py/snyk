"""Reference to SnykTenant model."""


class SnykTenantReference:
    """Reference to SnykTenant model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_tenant

        return snyk_tenant.SnykTenant
