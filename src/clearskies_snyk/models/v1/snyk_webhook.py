"""Snyk Webhook model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have
webhook management endpoints.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import String

from clearskies_snyk.backends import SnykV1Backend


class SnykWebhook(Model):
    """
    Model for Snyk Webhooks (v1 API).

    This model represents webhooks in a Snyk organization. Webhooks allow you
    to receive notifications when events occur in Snyk.

    Uses the Snyk v1 API endpoint: /org/{orgId}/webhooks

    ## Usage

    ```python
    from clearskies_snyk.models.v1 import SnykWebhook

    # Fetch all webhooks for an organization
    webhooks = SnykWebhook().where("org_id=org-id-123")
    for webhook in webhooks:
        print(f"Webhook: {webhook.url}")

    # Create a new webhook
    webhook = SnykWebhook()
    webhook.org_id = "org-id-123"
    webhook.url = "https://my.app.com/webhook-handler/snyk"
    webhook.secret = "my-secret-key"
    webhook.save()

    # Delete a webhook
    webhook.delete()
    ```

    ## Webhook Events

    Snyk sends a `ping` event to newly configured webhooks so you can verify
    the connection. You can also manually ping a webhook using the ping endpoint.

    ## Required Permissions

    - `View Organization`
    - `View Outbound Webhooks`
    - `Create Outbound Webhooks` (for creating)
    - `Remove Outbound Webhooks` (for deleting)
    """

    id_column_name: str = "id"
    backend = SnykV1Backend(can_update=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/webhooks"

    """
    The unique identifier for the webhook.
    """
    id = String()

    """
    The ID of the organization this webhook belongs to.
    """
    org_id = String(is_searchable=True)

    """
    The URL that Snyk will send webhook events to.
    Must use HTTPS protocol.
    """
    url = String()

    """
    A secret used to sign webhook payloads.
    Only used during creation - not returned in responses.
    Should be a random string with high entropy.
    """
    secret = String()
