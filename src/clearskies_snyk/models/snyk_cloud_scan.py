"""Snyk Cloud Scan model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Integer, Json, Select, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykCloudScan(Model):
    """
    Model for Snyk Cloud Scans.

    This model represents cloud scans in Snyk. Scans are triggered
    to analyze cloud environments for security issues.

    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/cloud/scans

    ```python
    from clearskies_snyk.models import SnykCloudScan

    # Fetch all cloud scans for an organization
    scans = SnykCloudScan().where("org_id=org-id-123")
    for scan in scans:
        print(f"Scan: {scan.id} ({scan.status})")

    # Access the parent organization
    print(f"Org: {scan.org.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/cloud/scans"

    """
    The unique identifier for the scan.
    """
    id = String()

    """
    The ID of the organization this scan belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        readable_parent_columns=["id", "name", "slug"],
        is_searchable=True,
    )

    """
    The parent organization this scan belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The ID of the environment being scanned.
    """
    environment_id = String()

    """
    The kind of scan.
    """
    kind = Select(
        allowed_values=[
            "scheduled",
            "user_initiated",
            "event_driven",
        ],
    )

    """
    The status of the scan.
    """
    status = Select(
        allowed_values=[
            "queued",
            "in_progress",
            "success",
            "error",
        ],
    )

    """
    Timestamp of when the scan was created.
    """
    created_at = Datetime()

    """
    Timestamp of when the scan was last updated.
    """
    updated_at = Datetime()

    """
    Timestamp of when the scan finished.
    """
    finished_at = Datetime()

    """
    Timestamp of when the scan was deleted (if applicable).
    """
    deleted_at = Datetime()

    """
    Increment for each change to a scan.
    """
    revision = Integer()

    """
    Error message if the scan failed.
    """
    error = String()

    """
    Errors that didn't fail the scan.
    """
    partial_errors = String()

    """
    Scan options.
    """
    options = Json()

    """
    Scan relationships.
    """
    relationships = Json()
