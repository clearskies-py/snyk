"""Reference to SnykOrgServiceAccount model."""


class SnykOrgServiceAccountReference:
    """Reference to SnykOrgServiceAccount model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_service_account

        return snyk_org_service_account.SnykOrgServiceAccount
