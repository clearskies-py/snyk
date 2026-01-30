"""Snyk Container Image model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Json, Select, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykContainerImage(Model):
    """
    Model for Snyk Container Images.

    This model represents container images in a Snyk organization.

    ```python
    from clearskies_snyk.models import SnykContainerImage

    # Fetch all container images for an organization
    images = SnykContainerImage().where("org_id=org-id-123")
    for image in images:
        print(f"Image: {image.names} ({image.platform})")

    # Access the parent organization
    print(f"Org: {image.org.name}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'resource_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "resource_type",
        }
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/container_images"

    """
    The unique identifier for the container image.
    """
    id = String()

    """
    The type of resource.
    """
    resource_type = Select(
        allowed_values=["container_image"],
    )

    """
    The platform of the container image.
    """
    platform = String()

    """
    The names of the container image.
    """
    names = String()

    """
    Image target references.
    """
    image_target_refs = Json()

    """
    The ID of the organization this container image belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        readable_parent_columns=["id", "name", "slug"],
        is_searchable=True,
    )

    """
    The parent organization this container image belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")
