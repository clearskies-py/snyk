"""Reference to SnykGroupTag model."""


class SnykGroupTagReference:
    """Reference to SnykGroupTag model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_group_tag

        return snyk_group_tag.SnykGroupTag
