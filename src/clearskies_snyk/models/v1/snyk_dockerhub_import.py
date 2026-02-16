"""Snyk Docker Hub Import model (v1 API).

This model is used to create import jobs for Docker Hub container images.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1Backend


class SnykDockerHubImport(Model):
    """
    Model for creating Docker Hub import jobs (v1 API).

    This model creates import jobs that import Docker Hub container images into Snyk for scanning.
    After creation, use SnykImportJob to check the import status.

    Uses the Snyk v1 API endpoint: POST /org/{orgId}/integrations/{integrationId}/import

    ## Usage

    ```python
    import clearskies
    from clearskies_snyk.models.v1 import SnykDockerHubImport, SnykImportJob


    def my_handler(snyk_dockerhub_import: SnykDockerHubImport, snyk_import_job: SnykImportJob):
        # Create an import job for a Docker Hub image
        import_response = snyk_dockerhub_import.create(
            {
                "org_id": "4a18d42f-0706-4ad0-b127-24078731fbed",
                "integration_id": "9a3e5d90-b782-468a-a042-9a2073736f0b",
                "target": {"name": "organization/repository:tag"},
            }
        )

        # Check import job status
        org_id = import_response.org_id
        integration_id = import_response.integration_id
        job = snyk_import_job.find(
            f"org_id={org_id}&integration_id={integration_id}&id={import_response.id}"
        )
    ```

    ## Target Object

    The target object specifies the Docker Hub image to import:
    - `name` (required): Image name including tag prefixed by organization name
      Format: `organization/repository:tag`
      Example: `"myorg/myapp:latest"`

    ## Required Permissions

    - `View Organization`
    - `Add Project`
    - `Test Project`
    """

    id_column_name: str = "id"
    backend = SnykV1Backend(can_update=False, can_delete=False, can_query=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/integrations/{integration_id}/import"

    """
    The unique identifier for the organization (required for routing).
    """
    org_id = String(is_searchable=True)

    """
    The unique identifier for the integration (required for routing).
    This can be found on the Integration page in the Settings area.
    """
    integration_id = String(is_searchable=True)

    """
    The target container image to import.
    Object with: name (required).
    Example: {"name": "organization/repository:tag"}
    """
    target = Json()
