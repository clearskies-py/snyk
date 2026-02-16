"""Snyk Org Policy Event model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Json, Select, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_policy_reference, snyk_org_reference


class SnykOrgPolicyEvent(Model):
    """
    Model for Snyk Organization Policy Events.

    This model represents the event history for a policy.
    Events track changes like creation, approval, rejection, etc.

    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/policies/{policy_id}/events

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrgPolicyEvent


    def my_handler(snyk_org_policy_event: SnykOrgPolicyEvent):
        # Fetch all events for a policy
        events = snyk_org_policy_event.where("org_id=org-id-123").where("policy_id=policy-id-456")
        for event in events:
            print(f"Event: {event.event_type} at {event.created_at}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/policies/{policy_id}/events"

    """
    The unique identifier for the event.
    """
    id = String()

    """
    The ID of the organization this event belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        is_searchable=True,
    )

    """
    The parent organization this event belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The ID of the policy this event belongs to.
    """
    policy_id = BelongsToId(
        snyk_org_policy_reference.SnykOrgPolicyReference,
        is_searchable=True,
    )

    """
    The parent policy this event belongs to.

    BelongsTo relationship to SnykOrgPolicy.
    """
    policy = BelongsToModel("policy_id")

    """
    The type of event.
    """
    event_type = Select(
        allowed_values=[
            "approve",
            "reject",
            "cancel",
            "reopen",
            "edit",
            "create",
        ],
    )

    """
    Timestamp of when the event was created.
    """
    created_at = Datetime()

    """
    Information about who created the event.
    """
    created_by = Json()

    """
    Optional comment associated with the event.
    """
    comment = String()

    """
    The changes made in this event.
    """
    changes = Json()
