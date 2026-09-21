"""Snyk Fix Pull Request model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference, snyk_project_reference


class SnykFixPullRequest(Model):
    """
    Model for Snyk Fix Pull Request.

    This model represents a Snyk Fix pull request that can be created to fix
    vulnerabilities in a project. This feature is currently in beta.
    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/projects/{project_id}/fix_pull_requests

    ```python
    import clearskies
    from clearskies_snyk.models import SnykFixPullRequest


    def my_handler(snyk_fix_pull_request: SnykFixPullRequest):
        # Create a fix pull request (POST only endpoint)
        # This is typically used to trigger PR creation for specific issues
        fix_pr = snyk_fix_pull_request
        fix_pr.save(
            {
                "org_id": "org-123",
                "project_id": "project-456",
                "issue_ids": ["SNYK-JS-YARGSPARSER-560381"],
            }
        )
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(
        resource_type="pull_request",
        api_to_model_map={"type": "pr_type"},
        can_update=False,
        can_delete=False,
        can_query=False,
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/projects/{project_id}/fix_pull_requests"

    # Columns based on the response schema
    id = String()  # Remediation job ID
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        is_searchable=True,
    )

    """
    The parent organization this fix pull request belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    project_id = BelongsToId(
        snyk_project_reference.SnykProjectReference,
        is_searchable=True,
    )

    """
    The parent project this fix pull request belongs to.

    BelongsTo relationship to SnykProject.
    """
    project = BelongsToModel("project_id")

    pr_type = String()  # Mapped from 'type', e.g., "resource"

    # Attributes from response
    status = String()  # STARTED, FINISHED, ERRORED
    created_at = Datetime()

    # Request attributes
    issue_ids = Json()  # Array of issue IDs to fix, e.g., ["SNYK-JS-YARGSPARSER-560381"]
