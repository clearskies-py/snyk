"""Reference to SnykGroupServiceAccount model."""


class SnykGroupServiceAccountReference:
    """Reference to SnykGroupServiceAccount model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_service_account

        return snyk_group_service_account.SnykGroupServiceAccount
