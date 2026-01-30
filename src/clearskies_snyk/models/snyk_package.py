"""Snyk Package model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykBackend


class SnykPackage(Model):
    """
    Model for Snyk Packages.

    This model represents package metadata from an ecosystem.
    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/ecosystems/{ecosystem}/packages/{package_name}

    ```python
    from clearskies_snyk.models import SnykPackage

    # Get package metadata
    package = SnykPackage().where("org_id=org-id-123&ecosystem=npm&package_name=express").first()
    print(f"Package: {package.package_name}")
    print(f"Latest Version: {package.latest_version}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'package_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "package_type",
        }
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/ecosystems/{ecosystem}/packages/{package_name}"

    """
    The unique identifier for the package (purl format).
    """
    id = String()

    """
    The ID of the organization.
    """
    org_id = String(is_searchable=True)

    """
    The ecosystem (e.g., npm, maven, pypi).
    """
    ecosystem = String(is_searchable=True)

    """
    The type of resource (package).
    """
    package_type = String()

    """
    The package ID in purl format.
    """
    package_id = String()

    """
    The name of the package.
    """
    package_name = String()

    """
    The programming language of the package.
    """
    language = String()

    """
    The description of the package.
    """
    description = String()

    """
    Keywords associated with the package.
    """
    keywords = Json()

    """
    The latest version of the package.
    """
    latest_version = String()

    """
    Package details including URLs.
    """
    package_details = Json()

    """
    Package health information.
    """
    package_health = Json()

    """
    Owner details.
    """
    owner_details = Json()
