"""Reference to SnykWebhook model."""


class SnykWebhookReference:
    """Reference to SnykWebhook model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_webhook

        return snyk_webhook.SnykWebhook
