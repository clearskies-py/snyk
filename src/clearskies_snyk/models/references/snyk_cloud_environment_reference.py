"""Reference to SnykCloudEnvironment model."""


class SnykCloudEnvironmentReference:
    """Reference to SnykCloudEnvironment model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_cloud_environment

        return snyk_cloud_environment.SnykCloudEnvironment
