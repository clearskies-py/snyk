"""Snyk Project History model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have a direct
equivalent endpoint for project history/snapshots.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Integer, Json, String

from clearskies_snyk.backends import SnykV1Backend
from clearskies_snyk.models.references import snyk_org_reference, snyk_project_reference


class SnykProjectHistory(Model):
    """
    Model for Snyk Project History (v1 API).

    This model represents the history of a Snyk project, including snapshots
    of issue counts and dependencies over time.
    Uses the Snyk v1 API endpoint: /org/{orgId}/project/{projectId}/history

    ```python
    import clearskies
    from clearskies_snyk.models import SnykProjectHistory


    def my_handler(snyk_project_history: SnykProjectHistory):
        # Fetch history for a project
        history = snyk_project_history.where("org_id=org-id-123").where("project_id=project-id-456")
        for snapshot in history:
            print(f"Snapshot: {snapshot.created} - Issues: {snapshot.issue_counts}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykV1Backend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/project/{project_id}/history"

    """
    The unique identifier for the history entry.
    """
    id = String()

    """
    Timestamp of when the snapshot was created.
    """
    created = Datetime()

    """
    The ID of the organization.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        is_searchable=True,
    )

    """
    The parent organization this history entry belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The ID of the group.
    """
    group_id = String()

    """
    The ID of the project.
    """
    project_id = BelongsToId(
        snyk_project_reference.SnykProjectReference,
        is_searchable=True,
    )

    """
    The parent project this history entry belongs to.

    BelongsTo relationship to SnykProject.
    """
    project = BelongsToModel("project_id")

    """
    Total number of dependencies.
    """
    total_dependencies = Integer()

    """
    Issue counts breakdown.
    """
    issue_counts = Json()

    """
    The container image ID (for container projects).
    """
    image_id = String()

    """
    The container image tag.
    """
    image_tag = String()

    """
    The container image platform.
    """
    image_platform = String()

    """
    The base image name.
    """
    base_image_name = String()

    """
    The method used for scanning.
    """
    method = String()

    """
    Group information.
    """
    group = Json()

    """
    Filters applied to the history query.
    """
    filters = Json(is_temporary=True)
