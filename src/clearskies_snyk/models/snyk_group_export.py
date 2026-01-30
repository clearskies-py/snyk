"""Snyk Group Export model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Datetime, Select, String

from clearskies_snyk.backends import SnykBackend


class SnykGroupExport(Model):
    """
    Model for Snyk Group Exports.

    This model represents data export jobs at the group level.
    Exports allow bulk extraction of data from Snyk for reporting
    and analysis purposes.

    Uses the Snyk v2 REST API endpoint: `/groups/{group_id}/export`

    ```python
    from clearskies_snyk.models import SnykGroupExport

    # Check export status
    export = SnykGroupExport().find("group_id=group-id-123", "export_id=export-id-456")
    print(f"Export Status: {export.status}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/export"

    """
    The unique identifier for the export job.
    """
    id = String()

    """
    The ID of the group this export belongs to.
    """
    group_id = String(is_searchable=True)

    """
    The status of the export job.
    """
    status = Select(allowed_values=["pending", "processing", "finished", "failed"])

    """
    The format of the export (e.g., csv, json).
    """
    format = String()

    """
    Timestamp of when the export was created.
    """
    created_at = Datetime()

    """
    Timestamp of when the export was completed.
    """
    finished_at = Datetime()

    """
    URL to download the export results.
    """
    download_url = String()
