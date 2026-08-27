"""Snyk Org Policy Event model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, Datetime, Json, Select, String

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

    """
    Name of the policy event.
    """
    name = String()

    """
    Timestamp when last updated.
    """
    updated_at = Datetime()

    """
    The action of the event.
    """
    action = String()

    """
    The type of action.
    """
    action_type = String()

    """
    Conditions group for the event.
    """
    conditions_group = Json()

    """
    Search by keyword.
    """
    search = String(is_searchable=True, is_temporary=True)

    """
    Sort field.
    """
    order_by = Select(
        allowed_values=["created", "expires", "ignore-type", "requested-by"], is_searchable=True, is_temporary=True
    )

    """
    Sort direction.
    """
    order_direction = Select(allowed_values=["asc", "desc"], is_searchable=True, is_temporary=True)

    """
    Filter by review status.
    """
    review_filter = String(is_searchable=True, is_temporary=True)

    """
    Filter by review status (maps to 'review' query param).
    """
    review = String(is_searchable=True, is_temporary=True)

    """
    Filter events expiring before this date.
    """
    expires_before = String(is_searchable=True, is_temporary=True)

    """
    Filter events expiring after this date.
    """
    expires_after = String(is_searchable=True, is_temporary=True)

    """
    Filter events that never expire.
    """
    expires_never = Boolean(is_searchable=True, is_temporary=True)

    """
    Filter by source.
    """
    source = String(is_searchable=True, is_temporary=True)
