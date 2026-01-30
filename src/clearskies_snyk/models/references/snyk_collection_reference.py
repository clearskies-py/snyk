"""Reference to SnykCollection model."""


class SnykCollectionReference:
    """Reference to SnykCollection model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_collection

        return snyk_collection.SnykCollection
