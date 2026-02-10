"""Project tag list column type."""

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable

from clearskies import decorators
from clearskies.columns import Json

if TYPE_CHECKING:
    from clearskies import typing


@dataclass
class SnykProjectTag:
    """
    Dataclass for Snyk project tags.

    Tags in Snyk are key-value pairs used to categorize and filter projects.
    """

    key: str
    value: str

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary for API serialization."""
        return {"key": self.key, "value": self.value}


class ProjectTagList(Json):
    """
    Column type for Snyk project tags.

    This column type handles the conversion between the API's tag format
    (list of {key, value} objects) and Python dataclass instances.

    ```python
    from clearskies import Model
    from clearskies_snyk.columns import ProjectTagList


    class MyProject(Model):
        tags = ProjectTagList()


    # When reading from the backend:
    # API returns: {"tags": [{"key": "env", "value": "prod"}]}
    # Model provides: model.tags = [SnykProjectTag(key="env", value="prod")]

    # When writing to the backend:
    # Model has: model.tags = [SnykProjectTag(key="env", value="prod")]
    # API receives: {"tags": [{"key": "env", "value": "prod"}]}
    ```
    """

    _descriptor_config_map = None

    @decorators.parameters_to_properties
    def __init__(
        self,
        default: dict[str, Any] | list[Any] | None = None,
        setable: dict[str, Any] | list[Any] | Callable[..., dict[str, Any]] | None = None,
        is_readable: bool = True,
        is_writeable: bool = True,
        is_temporary: bool = False,
        validators: "typing.validator | list[typing.validator]" = [],
        on_change_pre_save: "typing.action | list[typing.action]" = [],
        on_change_post_save: "typing.action | list[typing.action]" = [],
        on_change_save_finished: "typing.action | list[typing.action]" = [],
        created_by_source_type: str = "",
        created_by_source_key: str = "",
        created_by_source_strict: bool = True,
    ):
        pass

    def from_backend(self, value: Any) -> list[SnykProjectTag]:
        """
        Convert backend value to a list of SnykProjectTag instances.

        Handles both list of dicts and JSON string inputs.

        Args:
            value: Either a list of tag dicts or a JSON string.

        Returns:
            A list of SnykProjectTag instances.
        """
        tags: list[SnykProjectTag] = []
        if not value:
            return tags

        if isinstance(value, list):
            for tag in value:
                if isinstance(tag, dict):
                    tags.append(SnykProjectTag(**tag))
                elif isinstance(tag, SnykProjectTag):
                    tags.append(tag)
        elif isinstance(value, str):
            try:
                json_value = json.loads(value)
                for tag in json_value:
                    tags.append(SnykProjectTag(**tag))
            except json.JSONDecodeError:
                pass

        return tags

    def to_backend(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Convert SnykProjectTag instances to dicts for backend storage.

        Args:
            data: Dictionary containing the column data.

        Returns:
            Dictionary with the column value converted to list of dicts.
        """
        if self.name not in data:
            return data

        tag_data = data.get(self.name)
        if isinstance(tag_data, list):
            data[self.name] = [tag.to_dict() if isinstance(tag, SnykProjectTag) else tag for tag in tag_data]

        return data
