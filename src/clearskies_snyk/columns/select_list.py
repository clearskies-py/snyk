"""Select list column type for validated arrays."""

from typing import TYPE_CHECKING, Any, Callable

from clearskies import decorators
from clearskies.columns import Json

if TYPE_CHECKING:
    from clearskies import Model, typing


class SelectList(Json):
    """
    Column type for arrays with validated values.

    This column type handles arrays where each element must be one of a set of
    allowed values. It's used for Snyk API fields like business_criticality,
    environment, and lifecycle which are arrays of enum values.

    The Snyk API requires these fields to be arrays (e.g., ["critical"]) rather
    than single values. This column type ensures proper serialization while
    providing validation of allowed values.

    ```python
    from clearskies import Model
    from clearskies_snyk.columns import SelectList


    class MyProject(Model):
        business_criticality = SelectList(
            allowed_values=["critical", "high", "medium", "low"],
        )
        environment = SelectList(
            allowed_values=[
                "frontend",
                "backend",
                "internal",
                "external",
                "mobile",
                "saas",
                "onprem",
                "hosted",
                "distributed",
            ],
        )


    # When reading from the backend:
    # API returns: {"business_criticality": ["critical", "high"]}
    # Model provides: model.business_criticality = ["critical", "high"]

    # When writing to the backend:
    # Model has: model.business_criticality = ["critical"]
    # API receives: {"business_criticality": ["critical"]}
    ```
    """

    _descriptor_config_map = None
    allowed_values: list[str]

    @decorators.parameters_to_properties
    def __init__(
        self,
        allowed_values: list[str] | None = None,
        default: list[Any] | None = None,
        setable: list[Any] | Callable[..., list[Any]] | None = None,
        is_readable: bool = True,
        is_writeable: bool = True,
        is_temporary: bool = False,
        is_searchable: bool = False,
        validators: "typing.validator | list[typing.validator]" = [],
        on_change_pre_save: "typing.action | list[typing.action]" = [],
        on_change_post_save: "typing.action | list[typing.action]" = [],
        on_change_save_finished: "typing.action | list[typing.action]" = [],
        created_by_source_type: str = "",
        created_by_source_key: str = "",
        created_by_source_strict: bool = True,
    ):
        self.allowed_values = allowed_values or []

    def from_backend(self, value: Any) -> list[str]:
        """
        Convert backend value to a list of strings.

        Handles both list inputs and None values.

        Args:
            value: Either a list of strings or None.

        Returns:
            A list of strings (empty list if value is None/empty).
        """
        if not value:
            return []

        if isinstance(value, list):
            return [str(v) for v in value]

        # If it's a single value, wrap it in a list
        if isinstance(value, str):
            return [value]

        return []

    def to_backend(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Ensure the value is a list for backend storage.

        Args:
            data: Dictionary containing the column data.

        Returns:
            Dictionary with the column value as a list.
        """
        if self.name not in data:
            return data

        value = data.get(self.name)

        # Ensure value is a list
        if value is None:
            data[self.name] = []
        elif isinstance(value, str):
            # Single value passed as string - wrap in list
            data[self.name] = [value]
        elif isinstance(value, list):
            # Already a list, ensure all values are strings
            data[self.name] = [str(v) for v in value]

        return data

    def input_errors(self, model: "Model", data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate that all values in the list are allowed.

        Args:
            model: The model instance.
            data: Dictionary containing the input data.

        Returns:
            Dictionary with column name as key and list of error messages as value.
        """
        if self.name not in data:
            return {}

        value = data.get(self.name)

        if value is None:
            return {}

        # Handle single value passed as string
        if isinstance(value, str):
            value = [value]

        if not isinstance(value, list):
            return {self.name: f"'{self.name}' must be a list"}

        if self.allowed_values:
            invalid_values = [item for item in value if item not in self.allowed_values]
            if invalid_values:
                return {
                    self.name: (
                        f"Invalid value(s) for '{self.name}': {', '.join(invalid_values)}. "
                        f"Allowed values are: {', '.join(self.allowed_values)}"
                    )
                }

        return {}
