"""Snyk Project SBOM model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykBackend


class SnykProjectSbom(Model):
    """
    Model for Snyk Project SBOM Export.

    This model represents the SBOM (Software Bill of Materials) export
    for a project. It provides a standardized format for describing
    the components in a project.

    Uses the Snyk v2 REST API endpoint: `/orgs/{org_id}/projects/{project_id}/sbom`

    ```python
    from clearskies_snyk.models import SnykProjectSbom

    # Fetch SBOM for a project
    sbom = SnykProjectSbom().find("org_id=org-id-123", "project_id=project-id-456")
    print(f"SBOM Format: {sbom.format}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/projects/{project_id}/sbom"

    """
    The unique identifier (typically the project ID).
    """
    id = String()

    """
    The ID of the organization.
    """
    org_id = String(is_searchable=True)

    """
    The ID of the project.
    """
    project_id = String(is_searchable=True)

    """
    The SBOM format (e.g., CycloneDX, SPDX).
    """
    format = String()

    """
    The SBOM version.
    """
    version = String()

    """
    The SBOM document content.
    """
    sbom = Json()
