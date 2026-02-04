"""Snyk Group Audit Log model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_group_reference


class SnykGroupAuditLog(Model):
    """
    Model for Snyk Group Audit Logs.

    This model represents audit log entries at the group level in Snyk.
    Audit logs track various events like group creation, user management,
    policy changes, etc.

    Uses the Snyk v2 REST API endpoint: /groups/{group_id}/audit_logs/search

    ```python
    from clearskies_snyk.models import SnykGroupAuditLog

    # Fetch audit logs for a group
    logs = SnykGroupAuditLog().where("group_id=group-id-123")
    for log in logs:
        print(f"Event: {log.event} at {log.created}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/audit_logs/search"

    """
    The unique identifier for the audit log entry.
    """
    id = String()

    """
    The ID of the group this audit log belongs to.
    """
    group_id = BelongsToId(
        snyk_group_reference.SnykGroupReference,
        readable_parent_columns=["id", "name"],
        is_searchable=True,
    )

    """
    The parent group this audit log belongs to.

    BelongsTo relationship to SnykGroup.
    """
    group = BelongsToModel("group_id")

    """
    The event type (e.g., group.create, group.user.add).
    """
    event = String()

    """
    Timestamp of when the event occurred.
    """
    created = Datetime()

    """
    The organization ID associated with the event (if applicable).
    """
    org_id = String()

    """
    The project ID associated with the event (if applicable).
    """
    project_id = String()

    """
    The content/details of the audit log entry.
    """
    content = Json()
