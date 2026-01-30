"""Tests for the Snyk columns."""

from __future__ import annotations

import unittest

from clearskies_snyk.columns import ProjectTagList, SnykProjectTag


class TestProjectTagList(unittest.TestCase):
    """Tests for ProjectTagList column."""

    def test_from_backend_list_of_dicts(self) -> None:
        """Test conversion from list of dicts."""
        column = ProjectTagList()
        column.name = "tags"

        value = [
            {"key": "env", "value": "prod"},
            {"key": "team", "value": "security"},
        ]

        result = column.from_backend(value)

        assert len(result) == 2
        assert isinstance(result[0], SnykProjectTag)
        assert result[0].key == "env"
        assert result[0].value == "prod"
        assert result[1].key == "team"
        assert result[1].value == "security"

    def test_from_backend_json_string(self) -> None:
        """Test conversion from JSON string."""
        column = ProjectTagList()
        column.name = "tags"

        value = '[{"key": "env", "value": "prod"}]'

        result = column.from_backend(value)

        assert len(result) == 1
        assert result[0].key == "env"
        assert result[0].value == "prod"

    def test_from_backend_empty(self) -> None:
        """Test conversion from empty value."""
        column = ProjectTagList()
        column.name = "tags"

        result = column.from_backend(None)
        assert result == []

        result = column.from_backend([])
        assert result == []

    def test_to_backend(self) -> None:
        """Test conversion to backend format."""
        column = ProjectTagList()
        column.name = "tags"

        data = {
            "tags": [
                SnykProjectTag(key="env", value="prod"),
                SnykProjectTag(key="team", value="security"),
            ]
        }

        result = column.to_backend(data)

        assert len(result["tags"]) == 2
        assert result["tags"][0] == {"key": "env", "value": "prod"}
        assert result["tags"][1] == {"key": "team", "value": "security"}

    def test_to_backend_no_tags(self) -> None:
        """Test conversion when tags not in data."""
        column = ProjectTagList()
        column.name = "tags"

        data = {"name": "test"}

        result = column.to_backend(data)

        assert result == {"name": "test"}

    def test_from_backend_list_with_snyk_project_tag_instances(self) -> None:
        """Test conversion from list containing SnykProjectTag instances."""
        column = ProjectTagList()
        column.name = "tags"

        # When the list already contains SnykProjectTag instances
        value = [
            SnykProjectTag(key="env", value="prod"),
            {"key": "team", "value": "security"},  # Mix of dict and SnykProjectTag
        ]

        result = column.from_backend(value)

        assert len(result) == 2
        assert isinstance(result[0], SnykProjectTag)
        assert result[0].key == "env"
        assert result[0].value == "prod"
        assert isinstance(result[1], SnykProjectTag)
        assert result[1].key == "team"
        assert result[1].value == "security"

    def test_from_backend_invalid_json_string(self) -> None:
        """Test conversion from invalid JSON string returns empty list."""
        column = ProjectTagList()
        column.name = "tags"

        # Invalid JSON should be handled gracefully
        value = "not valid json {"

        result = column.from_backend(value)

        assert result == []


class TestSnykProjectTag(unittest.TestCase):
    """Tests for SnykProjectTag dataclass."""

    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        tag = SnykProjectTag(key="env", value="prod")

        result = tag.to_dict()

        assert result == {"key": "env", "value": "prod"}


if __name__ == "__main__":
    unittest.main()
