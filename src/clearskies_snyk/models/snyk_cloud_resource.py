"""Snyk Cloud Resource model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, BelongsToId, BelongsToModel, Datetime, Integer, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykCloudResource(Model):
    """
    Model for Snyk Cloud Resources.

    This model represents cloud resources discovered during scans.
    Resources are cloud infrastructure components like S3 buckets,
    EC2 instances, etc.

    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/cloud/resources

    ```python
    from clearskies_snyk.models import SnykCloudResource

    # Fetch all cloud resources for an organization
    resources = SnykCloudResource().where("org_id=org-id-123")
    for resource in resources:
        print(f"Resource: {resource.name} ({resource.resource_type})")

    # Access the parent organization
    print(f"Org: {resource.org.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/cloud/resources"

    """
    The unique identifier for the resource.
    """
    id = String()

    """
    The ID of the organization this resource belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        readable_parent_columns=["id", "name", "slug"],
        is_searchable=True,
    )

    """
    The parent organization this resource belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    Human friendly resource name.
    """
    name = String()

    """
    Kind of resource (e.g., runtime, cloud, iac).
    """
    kind = String()

    """
    Resource platform (e.g., aws, azure, google).
    """
    platform = String()

    """
    Terraform resource type (e.g., aws_s3_bucket).
    """
    resource_type = String()

    """
    Unique ID for the resource.
    """
    resource_id = String()

    """
    ID of the physical resource from the cloud provider (e.g., AWS ARN).
    """
    native_id = String()

    """
    Physical location (e.g., AWS region).
    """
    location = String()

    """
    Resource namespace (e.g., AWS region).
    """
    namespace = String()

    """
    Computed hash value for the resource based on its attributes.
    """
    hash = String()

    """
    Increment for each change to a resource.
    """
    revision = Integer()

    """
    Whether the resource is managed.
    """
    is_managed = Boolean()

    """
    Timestamp of when the resource was first recorded.
    """
    created_at = Datetime()

    """
    Timestamp of when the resource was last updated.
    """
    updated_at = Datetime()

    """
    Timestamp of when the resource was deleted (if applicable).
    """
    deleted_at = Datetime()

    """
    Timestamp of when the resource was removed (if applicable).
    """
    removed_at = Datetime()

    """
    Terraform state attributes.
    """
    state = Json()

    """
    Resource tags from the cloud provider.
    """
    tags = Json()

    """
    Resource relationships.
    """
    relationships = Json()

    """
    Source location information.
    """
    source_location = Json()
