"""Reference to SnykIntegration model."""


class SnykIntegrationReference:
    """Reference to SnykIntegration model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_integration

        return snyk_integration.SnykIntegration
