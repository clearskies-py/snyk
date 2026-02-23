"""Snyk Import Job model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have
import job endpoints.
"""

from dataclasses import dataclass
from typing import Any, Self, cast

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1Backend


@dataclass
class ImportProject:
    """
    Represents a project created from an import target.

    Attributes:
        target_file: The project's package manifest file
        success: Whether the project was successfully imported
        project_url: The URL to the project in Snyk
        project_id: The Snyk project public ID
    """

    target_file: str
    success: bool
    project_url: str
    project_id: str


@dataclass
class ImportLog:
    """
    Represents a single log entry for a target being imported.

    Attributes:
        name: The name of the target (e.g., 'org/repo')
        created: Timestamp when import was attempted
        status: Status of this specific import
        truncated: Whether the import was truncated
        projects: List of projects created from this target
    """

    name: str
    created: str
    status: str
    truncated: bool
    projects: list[ImportProject]


class SnykImportJob(Model):
    """
    Model for Snyk Import Jobs (v1 API).

    This model represents import jobs that import targets (repositories,
    container images, etc.) into Snyk for scanning. This model is used to
    check the status of import jobs, not to create them.

    To create import jobs, use one of the dedicated import models:
    - `SnykGitHubImport` for GitHub/GitHub Enterprise repositories
    - `SnykGitLabImport` for GitLab repositories
    - `SnykBitbucketCloudImport` for Bitbucket Cloud repositories
    - `SnykBitbucketServerImport` for Bitbucket Server repositories
    - `SnykAzureReposImport` for Azure Repos repositories
    - `SnykDockerHubImport` for Docker Hub images
    - `SnykContainerRegistryImport` for other container registries

    Uses the Snyk v1 API endpoint: /org/{orgId}/integrations/{integrationId}/import/{jobId}

    ## Usage

    ```python
    import clearskies
    from clearskies_snyk.models.v1 import SnykGitHubImport, SnykImportJob

    # Build the DI container
    di = clearskies.di.StandardDependencies()

    # Create an import job
    github_import = di.build(SnykGitHubImport)
    import_job = github_import.create(
        {
            "org_id": "4a18d42f-0706-4ad0-b127-24078731fbed",
            "integration_id": "9a3e5d90-b782-468a-a042-9a2073736f0b",
            "target": {"owner": "my-org", "name": "my-repo", "branch": "main"},
        }
    )

    # Check the import job status
    import_job_model = di.build(
        SnykImportJob, org_id=import_job.org_id, integration_id=import_job.integration_id
    )
    job = import_job_model.find(import_job.job_id)
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
    """

    id_column_name: str = "job_id"
    backend = SnykV1Backend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/integrations/{integration_id}/import"

    """
    The unique identifier for the import job.
    """
    job_id = String()

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

    def get_logs(self) -> list[ImportLog]:
        """
        Get the import logs as a list of ImportLog dataclass instances.

        Returns:
            list[ImportLog]: List of ImportLog objects representing each target import log.

        Example:
            ```python
            job = import_job_model.find(job_id)
            for log in job.get_logs():
                print(f"{log.name}: {log.status}")
                for project in log.projects:
                    success_str = "✓" if project.success else "✗"
                    print(f"  {success_str} {project.target_file} ({project.project_id})")
            ```
        """
        raw_logs = cast(list[dict[str, Any]], self.logs or [])
        return [
            ImportLog(
                name=log.get("name", ""),
                created=log.get("created", ""),
                status=log.get("status", ""),
                truncated=log.get("truncated", False),
                projects=[
                    ImportProject(
                        target_file=proj.get("targetFile", ""),
                        success=proj.get("success", False),
                        project_url=proj.get("projectUrl", ""),
                        project_id=proj.get("projectId", ""),
                    )
                    for proj in log.get("projects", [])
                ],
            )
            for log in raw_logs
        ]
