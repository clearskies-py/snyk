"""Snyk Container Image Target Ref model."""

from typing import Self

from clearskies import Model
from clearskies.columns import String

from clearskies_snyk.backends import SnykBackend


class SnykContainerImageTargetRef(Model):
    """
    Model for Snyk Container Image Target References.

    This model represents target references for container images.

    ```python
    import clearskies
    from clearskies_snyk.models import SnykContainerImageTargetRef


    def my_handler(snyk_container_image_target_ref: SnykContainerImageTargetRef):
        # Fetch target refs for a container image
        refs = snyk_container_image_target_ref.where("org_id=org-id-123").where("id=image-id-456")
        for ref in refs:
            print(f"Target: {ref.target_id} - {ref.target_reference}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/container_images/{id}/relationships/image_target_refs"

    """
    The unique identifier for the target reference.
    """
    id = String(is_searchable=True)

    """
    The platform of the container image.
    """
    platform = String()

    """
    The ID of the organization.
    """
    org_id = String(is_searchable=True)

    """
    The ID of the target.
    """
    target_id = String()

    """
    The target reference (e.g., tag, digest).
    """
    target_reference = String()
