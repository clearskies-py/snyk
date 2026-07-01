"""Reference to SnykWebhook model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.v1.snyk_webhook import SnykWebhook


class SnykWebhookReference(ModelClassReference["SnykWebhook"]):
    """Reference to SnykWebhook model."""

    def get_model_class(self) -> type["SnykWebhook"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_webhook

        return snyk_webhook.SnykWebhook
