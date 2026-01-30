"""Reference to SnykEntitlement model."""


class SnykEntitlementReference:
    """Reference to SnykEntitlement model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_entitlement

        return snyk_entitlement.SnykEntitlement
