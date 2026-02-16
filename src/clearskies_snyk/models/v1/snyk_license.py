"""Snyk License model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have
a direct equivalent for listing licenses across an organization.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1Backend


class SnykLicense(Model):
    """
    Model for Snyk Licenses (v1 API).

    This model represents licenses found in dependencies across your projects.
    It provides information about license compliance and associated dependencies.

    Uses the Snyk v1 API endpoint: POST /org/{orgId}/licenses

    ## Usage

    ```python
    import clearskies
    from clearskies_snyk.models.v1 import SnykLicense


    def my_handler(snyk_license: SnykLicense):
        # Fetch all licenses for an organization
        licenses = snyk_license.where("org_id=org-id-123")
        for license in licenses:
            print(f"{license.id}: severity={license.severity}")
    ```

    ## Severity Levels

    License severity can be:
    - `none`: No compliance concern
    - `low`: Low compliance concern
    - `medium`: Medium compliance concern
    - `high`: High compliance concern

    ## Required Permissions

    - `View Organization`
    - `View Project`
    - `View Project Snapshot`
    """

    id_column_name: str = "id"
    backend = SnykV1Backend(can_update=False, can_delete=False, can_query=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/licenses"

    """
    The identifier of the license (e.g., 'MIT', 'Apache-2.0', 'GPL-3.0').
    """
    id = String()

    """
    The ID of the organization this license belongs to.
    """
    org_id = String(is_searchable=True)

    """
    The severity assigned to this license.
    One of: 'none', 'low', 'medium', 'high'.
    """
    severity = String()

    """
    Custom instructions assigned to this license by the organization.
    """
    instructions = String()

    """
    The dependencies that have this license.
    Each dependency has: id, name, version, packageManager.
    """
    dependencies = Json()

    """
    The projects which contain dependencies with this license.
    Each project has: id, name.
    """
    projects = Json()
