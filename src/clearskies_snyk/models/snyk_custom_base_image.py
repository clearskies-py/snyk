"""Snyk Custom Base Image model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Json, String

from clearskies_snyk.backends import SnykBackend


class SnykCustomBaseImage(Model):
    """
    Model for Snyk Custom Base Image.

    This model represents a custom base image that can be used for base image upgrade
    recommendations in container scanning.
    Uses the Snyk v2 REST API endpoint: /custom_base_images/{custombaseimage_id}

    ```python
    from clearskies_snyk.models import SnykCustomBaseImage

    # List custom base images
    images = SnykCustomBaseImage().where("org_id=org-123")
    for image in images:
        print(f"Image: {image.repository}:{image.tag}, Include: {image.include_in_recommendations}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(api_to_model_map={"type": "image_type"})

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "custom_base_images"

    # Columns based on CustomBaseImageResource schema
    id = String()
    image_type = String()  # Mapped from 'type', e.g., "custom_base_image"

    # Query parameters for filtering
    org_id = String(is_searchable=True)
    group_id = String(is_searchable=True)
    project_id = String(is_searchable=True)

    # Attributes from CustomBaseImageAttributes
    include_in_recommendations = Boolean()  # Whether this image should be recommended as a base image upgrade
    repository = String()  # Repository name
    tag = String()  # Image tag

    # Versioning schema (complex object)
    versioning_schema = Json()  # Can be semver, custom, or single-selection type
