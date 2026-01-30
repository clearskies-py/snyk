"""Reference to SnykContainerImage model."""


class SnykContainerImageReference:
    """Reference to SnykContainerImage model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_container_image

        return snyk_container_image.SnykContainerImage
