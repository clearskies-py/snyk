"""Snyk Learn Catalog model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Datetime, Integer, Json, Select, String

from clearskies_snyk.backends import SnykBackend


class SnykLearnCatalog(Model):
    """
    Model for Snyk Learn Catalog.

    This model represents catalog resources (lessons and learning paths) from Snyk Learn.
    Uses the Snyk v2 REST API endpoint: /learn/catalog

    ```python
    import clearskies
    from clearskies_snyk.models import SnykLearnCatalog


    def my_handler(snyk_learn_catalog: SnykLearnCatalog):
        # List all catalog resources
        resources = snyk_learn_catalog
        for resource in resources:
            print(f"Resource: {resource.name} ({resource.resource_type})")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'resource_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "resource_type",
        },
        can_create=False,
        can_update=False,
        can_delete=False,
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "learn/catalog"

    """
    The unique identifier for the catalog resource.
    """
    id = String()

    """
    The type of resource (lesson or learning_path).
    """
    resource_type = Select(allowed_values=["lesson", "learning_path"])

    """
    The name of the resource.
    """
    name = String()

    """
    The description of the resource.
    """
    description = String()

    """
    The URL to the resource.
    """
    url = String()

    """
    The slug for the resource.
    """
    slug = String()

    """
    The image URL for the resource.
    """
    image = String()

    """
    The education content category.
    """
    education_content_category = Select(allowed_values=["security education", "product training"])

    """
    Tags associated with the resource.
    """
    tags = Json()

    """
    The author of the resource.
    """
    author = String()

    """
    The date the resource was published.
    """
    date_published = Datetime()

    """
    The estimated duration in minutes.
    """
    estimated_duration = Integer()

    """
    The SEO title for the resource.
    """
    seo_title = String()

    """
    Lesson IDs for learning paths.
    """
    lesson_ids = Json()
