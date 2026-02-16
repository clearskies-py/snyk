"""Snyk Container Registry Import model (v1 API).

This model is used to create import jobs for various container registry platforms.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1Backend


class SnykContainerRegistryImport(Model):
    """
    Model for creating container registry import jobs (v1 API).

    This model creates import jobs that import container images from various
    container registry platforms into Snyk for scanning.

    Supported registries:
    - Google Container Registry (GCR)
    - Google Artifact Registry (GAR)
    - Harbor
    - DigitalOcean Container Registry
    - Quay
    - GitLab Container Registry
    - GitHub Container Registry
    - Azure Container Registry (ACR)
    - Elastic Container Registry (ECR)
    - Artifactory Container Registry
    - Nexus

    Uses the Snyk v1 API endpoint: POST /org/{orgId}/integrations/{integrationId}/import

    ## Usage

    ```python
    import clearskies
    from clearskies_snyk.models.v1 import SnykContainerRegistryImport, SnykImportJob


    def my_handler(
        snyk_container_registry_import: SnykContainerRegistryImport, snyk_import_job: SnykImportJob
    ):
        # Create an import job for a GCR/GAR/Harbor/etc. image
        import_response = snyk_container_registry_import.create(
            {
                "org_id": "4a18d42f-0706-4ad0-b127-24078731fbed",
                "integration_id": "9a3e5d90-b782-468a-a042-9a2073736f0b",
                "target": {"name": "project/repository:tag"},
            }
        )

        # For ACR/ECR/Artifactory/Nexus (no project prefix)
        import_response = snyk_container_registry_import.create(
            {
                "org_id": "4a18d42f-0706-4ad0-b127-24078731fbed",
                "integration_id": "9a3e5d90-b782-468a-a042-9a2073736f0b",
                "target": {"name": "repository:tag"},
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

    The target object specifies the container image to import:
    - `name` (required): Image name including tag

    The name format depends on the registry type:

    **GCR/GAR/Harbor/DigitalOcean/Quay/GitLab CR/GitHub CR:**
    - Format: `project/repository:tag` or `project-name/repository:tag`
    - Example: `"my-project/my-app:latest"`

    **ACR/ECR/Artifactory/Nexus:**
    - Format: `repository:tag`
    - Example: `"my-app:latest"`

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

    Format varies by registry:
    - GCR/GAR/Harbor/DigitalOcean/Quay/GitLab CR/GitHub CR: {"name": "project/repository:tag"}
    - ACR/ECR/Artifactory/Nexus: {"name": "repository:tag"}
    """
    target = Json()
