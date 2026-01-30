"""Snyk Collection Relationship Project model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, Select, String

from clearskies_snyk.backends import SnykBackend


class SnykCollectionRelationshipProject(Model):
    """
    Model for Snyk Collection Relationship Projects.

    This model represents the relationship between collections and projects.

    ```python
    from clearskies_snyk.models import SnykCollectionRelationshipProject

    # Fetch all projects in a collection
    relationships = SnykCollectionRelationshipProject().where("org_id=org-id-123").where("collection_id=col-id-456")
    for rel in relationships:
        print(f"Project: {rel.id}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/collections/{collection_id}/relationships/projects"

    """
    The unique identifier for the project.
    """
    id = String()

    """
    The ID of the organization.
    """
    org_id = String(is_searchable=True)

    """
    The ID of the collection.
    """
    collection_id = String(is_searchable=True)

    """
    The ID of the target.
    """
    target_id = String()

    """
    What to show in the collection.
    """
    show = Select(
        allowed_values=[
            "vuln-groups",
            "clean-groups",
        ],
    )

    """
    Metadata about the relationship.
    """
    meta = Json()
