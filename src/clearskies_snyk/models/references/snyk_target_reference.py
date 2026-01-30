"""Reference to SnykTarget model."""


class SnykTargetReference:
    """Reference to SnykTarget model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_target

        return snyk_target.SnykTarget
