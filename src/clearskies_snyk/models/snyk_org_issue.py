"""Snyk Org Issue model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, Datetime, Integer, Json, Select, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykOrgIssue(Model):
    """
    Model for Snyk Organization Issues.

    This model represents issues at the organization level in Snyk.

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrgIssue


    def my_handler(snyk_org_issue: SnykOrgIssue):
        # Fetch all issues for an organization
        issues = snyk_org_issue.where("org_id=org-id-123")
        for issue in issues:
            print(f"Issue: {issue.title} ({issue.effective_severity_level})")

        # Filter by scan item
        issues = (
            snyk_org_issue.where("org_id=org-id-123")
            .where("scan_item_id=project-123")
            .where("scan_item_type=project")
        )

        # Access the parent organization
        print(f"Org: {issue.org.name}")
    ```
    """

    id_column_name: str = "id"

    # Issues API uses scan_item.id and scan_item.type as query parameters
    # Map 'type' to 'issue_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "scan_item_id": "scan_item.id",
            "scan_item_type": "scan_item.type",
            "type": "issue_type",
        },
        can_create=False,
        can_update=False,
        can_delete=False,
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/issues"

    """
    The unique identifier for the issue.
    """
    id = String()

    """
    The ID of the organization this issue belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        is_searchable=True,
    )

    """
    The parent organization this issue belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The ID of the project this issue belongs to.
    """
    project_id = String()

    """
    The ID of the group this issue belongs to.
    """
    group_id = String()

    """
    The ID of the environment this issue belongs to.
    """
    environment_id = String()

    """
    Timestamp of when the issue was created.
    """
    created_at = Datetime()

    """
    Description of the issue.
    """
    description = String()

    """
    Coordinates of the issue.
    """
    coordinates = Json()

    """
    Representations of the issue.
    """
    representations = Json()

    """
    Classes of the issue.
    """
    classes = Json()

    """
    The effective severity level of the issue.
    """
    effective_severity_level = String()

    """
    Whether the issue is ignored.
    """
    ignored = Boolean()

    """
    The key of the issue.
    """
    key = String()

    """
    SAST identifier that allows the identification of Snyk Code issues with a unique ID per repository.
    """
    key_asset = String()

    """
    Priority information for the issue.
    """
    priority = Json()

    """
    Problems associated with the issue.
    """
    problems = Json()

    """
    The status of the issue.
    """
    status = String()

    """
    The title of the issue.
    """
    title = String()

    """
    The tool that detected the issue.
    """
    tool = String()

    """
    Resolution information for the issue.
    """
    resolution = Json()

    """
    Severities of the issue.
    """
    severities = Json()

    """
    Risk information for the issue.
    """
    risk = Json()

    """
    Exploit details for the issue, including maturity levels and sources.
    """
    exploit_details = Json()

    """
    The type of issue.
    """
    issue_type = Select(
        allowed_values=[
            "package_vulnerability",
            "license",
            "cloud",
            "code",
            "custom",
            "config",
            "secrets",
        ],
    )

    """
    Timestamp of when the issue was last updated.
    """
    updated_at = String()

    """
    The ID of the scan item.
    """
    scan_item_id = String()

    """
    The type of scan item.
    """
    scan_item_type = Select(
        allowed_values=[
            "project",
            "environment",
        ],
    )

    """
    Filter: Issues updated before this timestamp.
    """
    updated_before = Datetime(is_searchable=True, is_temporary=True)

    """
    Filter: Issues updated after this timestamp.
    """
    updated_after = Datetime(is_searchable=True, is_temporary=True)

    """
    Filter: Issues created before this timestamp.
    """
    created_before = Datetime(is_searchable=True, is_temporary=True)

    """
    Filter: Issues created after this timestamp.
    """
    created_after = Datetime(is_searchable=True, is_temporary=True)

    """
    Whether to include code flows in the response.
    """
    include_code_flows = Boolean(is_searchable=True, is_temporary=True)

    """
    Pagination offset.
    """
    offset = Integer(is_searchable=True, is_temporary=True)
