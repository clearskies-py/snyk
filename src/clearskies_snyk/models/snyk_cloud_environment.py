"""Snyk Cloud Environment model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Integer, Json, Select, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykCloudEnvironment(Model):
    """
    Model for Snyk Cloud Environments.

    This model represents cloud environments in Snyk. Cloud environments
    are connections to cloud providers (AWS, Azure, Google) for scanning.

    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/cloud/environments

    ```python
    import clearskies
    from clearskies_snyk.models import SnykCloudEnvironment


    def my_handler(snyk_cloud_environment: SnykCloudEnvironment):
        # Fetch all cloud environments for an organization
        environments = snyk_cloud_environment.where("org_id=org-id-123")
        for env in environments:
            print(f"Environment: {env.name} ({env.kind})")

        # Access the parent organization
        print(f"Org: {env.org.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/cloud/environments"

    """
    The unique identifier for the environment.
    """
    id = String()

    """
    The ID of the organization this environment belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        is_searchable=True,
    )

    """
    The parent organization this environment belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The name of the environment.
    """
    name = String()

    """
    The kind of cloud environment.
    """
    kind = Select(
        allowed_values=[
            "aws",
            "google",
            "azure",
            "scm",
            "tfc",
            "cli",
        ],
    )

    """
    Timestamp of when the environment was created.
    """
    created_at = Datetime()

    """
    Timestamp of when the environment was last updated.
    """
    updated_at = Datetime()

    """
    Timestamp of when the environment was deleted (if applicable).
    """
    deleted_at = Datetime()

    """
    Increment for each change to an environment.
    """
    revision = Integer()

    """
    Environment options (e.g., role_arn for AWS).
    """
    options = Json()

    """
    Environment properties (e.g., account_id).
    """
    properties = Json()

    """
    Environment relationships.
    """
    relationships = Json()
