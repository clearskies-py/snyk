"""Snyk Collection model."""

from typing import Self

from clearskies import Model
from clearskies.columns import (
    BelongsToId,
    BelongsToModel,
    Boolean,
    Json,
    ManyToManyIds,
    ManyToManyModels,
    String,
)

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models import snyk_collection_relationship_project
from clearskies_snyk.models.references import (
    snyk_org_reference,
    snyk_project_reference,
)


class SnykCollection(Model):
    """
    Model for Snyk Collections.

    This model represents collections in a Snyk organization. Collections are
    used to group projects together.

    ```python
    from clearskies_snyk.models import SnykCollection

    # Fetch all collections for an organization
    collections = SnykCollection().where("org_id=org-id-123")
    for collection in collections:
        print(f"Collection: {collection.name}")

    # Access the parent organization
    print(f"Org: {collection.org.name}")

    # Access related projects (ManyToMany)
    for project in collection.projects:
        print(f"  Project: {project.name}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'collection_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "collection_type",
        }
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/collections"

    """
    The unique identifier for the collection.
    """
    id = String()

    """
    The type of collection.
    """
    collection_type = String()

    """
    The name of the collection.
    """
    name = String()

    """
    Whether the collection is auto-generated.
    """
    is_generated = Boolean()

    """
    Metadata about the collection.
    """
    meta = Json()

    """
    The ID of the organization this collection belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        is_searchable=True,
    )

    """
    The parent organization this collection belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The IDs of projects in this collection.

    ManyToMany relationship to SnykProject via SnykCollectionRelationshipProject.
    """
    project_ids = ManyToManyIds(
        related_model_class=snyk_project_reference.SnykProjectReference,
        pivot_model_class=snyk_collection_relationship_project.SnykCollectionRelationshipProject,
        own_column_name_in_pivot="collection_id",
        related_column_name_in_pivot="id",
    )

    """
    Projects in this collection.

    ManyToMany relationship to SnykProject.
    """
    projects = ManyToManyModels("project_ids")
