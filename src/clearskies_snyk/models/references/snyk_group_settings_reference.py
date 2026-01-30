"""Reference to SnykGroupSettings model."""


class SnykGroupSettingsReference:
    """Reference to SnykGroupSettings model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_group_settings

        return snyk_group_settings.SnykGroupSettings
