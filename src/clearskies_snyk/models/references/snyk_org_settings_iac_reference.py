"""Reference to SnykOrgSettingsIac model."""


class SnykOrgSettingsIacReference:
    """Reference to SnykOrgSettingsIac model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_settings_iac

        return snyk_org_settings_iac.SnykOrgSettingsIac
