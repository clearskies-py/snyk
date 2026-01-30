"""Snyk Org Audit Log model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykOrgAuditLog(Model):
    """
    Model for Snyk Organization Audit Logs.

    This model represents audit log entries at the organization level in Snyk.
    Audit logs track various events like org creation, user management,
    project changes, etc.

    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/audit_logs/search

    ```python
    from clearskies_snyk.models import SnykOrgAuditLog

    # Fetch audit logs for an organization
    logs = SnykOrgAuditLog().where("org_id=org-id-123")
    for log in logs:
        print(f"Event: {log.event} at {log.created}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/audit_logs/search"

    """
    The unique identifier for the audit log entry.
    """
    id = String()

    """
    The ID of the organization this audit log belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        readable_parent_columns=["id", "name", "slug"],
        is_searchable=True,
    )

    """
    The parent organization this audit log belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The event type (e.g., org.create, org.user.add).
    """
    event = String()

    """
    Timestamp of when the event occurred.
    """
    created = Datetime()

    """
    The group ID associated with the event (if applicable).
    """
    group_id = String()

    """
    The project ID associated with the event (if applicable).
    """
    project_id = String()

    """
    The content/details of the audit log entry.
    """
    content = Json()
