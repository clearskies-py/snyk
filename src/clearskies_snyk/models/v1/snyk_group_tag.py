"""Snyk Group Tag model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have
a direct equivalent for group-level tag management.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import String

from clearskies_snyk.backends import SnykV1Backend


class SnykGroupTag(Model):
    """
    Model for Snyk Group Tags (v1 API).

    This model represents tags that can be applied to projects within a group.
    Tags are key-value pairs used for organizing and filtering projects.

    Uses the Snyk v1 API endpoint: /group/{groupId}/tags

    ## Usage

    ```python
    import clearskies
    from clearskies_snyk.models.v1 import SnykGroupTag


    def my_handler(snyk_group_tag: SnykGroupTag):
        # Fetch all tags for a group
        tags = snyk_group_tag.where("group_id=group-id-123")
        for tag in tags:
            print(f"Tag: {tag.key}={tag.value}")
    ```

    ## Tag Structure

    Tags consist of:
    - `key`: The tag category (e.g., 'environment', 'team')
    - `value`: The tag value (e.g., 'production', 'backend')

    ## Required Permissions

    - Admin access to the group
    """

    id_column_name: str = "id"
    backend = SnykV1Backend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "group/{group_id}/tags"

    """
    A composite identifier for the tag (key:value).
    """
    id = String()

    """
    The ID of the group this tag belongs to.
    """
    group_id = String(is_searchable=True)

    """
    The tag key (category).
    """
    key = String()

    """
    The tag value.
    """
    value = String()
