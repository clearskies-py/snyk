"""Reference to SnykProject model."""


class SnykProjectReference:
    """Reference to SnykProject model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_project

        return snyk_project.SnykProject
