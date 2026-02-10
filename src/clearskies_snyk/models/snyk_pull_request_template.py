"""Snyk Pull Request Template model."""

from typing import Self

from clearskies import Model
from clearskies.columns import String

from clearskies_snyk.backends import SnykBackend


class SnykPullRequestTemplate(Model):
    """
    Model for Snyk Pull Request Templates.

    This model represents pull request templates at the group level.
    Templates define the title, description, and commit message for Snyk PRs.
    Uses the Snyk v2 REST API endpoint: /groups/{group_id}/settings/pull_request_template

    ```python
    from clearskies_snyk.models import SnykPullRequestTemplate

    # Fetch pull request template for a group
    template = SnykPullRequestTemplate().where("group_id=group-id-123").first()
    print(f"PR Title: {template.title}")
    print(f"PR Description: {template.description}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'template_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "template_type",
        },
        can_update=False,
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/settings/pull_request_template"

    """
    The unique identifier for the template (URL format).
    """
    id = String()

    """
    The ID of the group this template belongs to.
    """
    group_id = String(is_searchable=True)

    """
    The type of resource (pull_request_template).
    """
    template_type = String()

    """
    The title template for pull requests.
    Supports template variables like {{package_name}}, {{package_from}}, {{package_to}}.
    """
    title = String()

    """
    The description template for pull requests.
    Supports template variables and conditionals like {{ #is_upgrade_pr }}.
    """
    description = String()

    """
    The commit message template for pull requests.
    Supports template variables like {{package_name}}, {{package_from}}, {{package_to}}.
    """
    commit_message = String()
