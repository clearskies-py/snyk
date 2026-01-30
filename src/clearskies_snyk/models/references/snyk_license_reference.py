"""Reference to SnykLicense model."""


class SnykLicenseReference:
    """Reference to SnykLicense model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_license

        return snyk_license.SnykLicense
