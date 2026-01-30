"""Reference to SnykDependency model."""


class SnykDependencyReference:
    """Reference to SnykDependency model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_dependency

        return snyk_dependency.SnykDependency
