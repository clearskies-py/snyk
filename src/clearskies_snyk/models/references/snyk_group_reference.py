"""Reference to SnykGroup model."""


class SnykGroupReference:
    """Reference to SnykGroup model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group

        return snyk_group.SnykGroup
