"""Snyk Import Job model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have
import job endpoints.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1Backend


class SnykImportJob(Model):
    """
    Model for Snyk Import Jobs (v1 API).

    This model represents import jobs that import targets (repositories,
    container images, etc.) into Snyk for scanning.

    Uses the Snyk v1 API endpoint: /org/{orgId}/integrations/{integrationId}/import/{jobId}

    ## Usage

    ```python
    from clearskies_snyk.models.v1 import SnykImportJob

    # Get import job status
    job = SnykImportJob().find("job-id-123")
    print(f"Status: {job.status}")
    for log in job.logs:
        print(f"  {log['name']}: {log['status']}")
    ```

    ## Job Status

    Import jobs can have the following statuses:
    - `pending`: Job is still processing
    - `complete`: Job finished successfully
    - `failed`: Job failed
    - `aborted`: Job was aborted

    ## Required Permissions

    - `View Organization`
    - `Add Project` (for creating import jobs)
    - `Test Project` (for creating import jobs)
    """

    id_column_name: str = "id"
    backend = SnykV1Backend(can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/integrations/{integration_id}/import"

    """
    The unique identifier for the import job.
    """
    id = String()

    """
    The ID of the organization this import job belongs to.
    """
    org_id = String(is_searchable=True)

    """
    The ID of the integration used for this import.
    """
    integration_id = String(is_searchable=True)

    """
    The status of the import job.
    One of: 'pending', 'complete', 'failed', 'aborted'.
    """
    status = String()

    """
    The timestamp when the import job was created (ISO-8601 format).
    """
    created = String()

    """
    Logs for each target being imported.
    Each log entry has:
    - name: The name of the target (e.g., 'org/repo')
    - created: Timestamp when import was attempted
    - status: Status of this specific import
    - truncated: Whether the import was truncated
    - projects: List of projects created from this target
    """
    logs = Json()
