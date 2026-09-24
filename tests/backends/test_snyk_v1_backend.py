"""Tests for SnykV1Backend."""

import clearskies

from clearskies_snyk.backends import SnykV1Backend


class TestSnykV1Backend:
    """Tests for the SnykV1Backend class."""

    def test_default_base_url(self):
        """Test that the default base URL is set correctly."""
        backend = SnykV1Backend()
        assert backend.base_url == "https://api.snyk.io/v1/"

    def test_default_api_casing(self):
        """Test that the default API casing is camelCase."""
        backend = SnykV1Backend()
        assert backend.api_casing == "camelCase"

    def test_default_pagination_parameters(self):
        """Test that the default pagination parameters are set correctly."""
        backend = SnykV1Backend()
        assert backend.pagination_parameter_name == "page"
        assert backend.limit_parameter_name == "perPage"

    def test_headers_config(self):
        """Test that headers include Content-Type."""
        backend = SnykV1Backend()
        assert backend.headers["Content-Type"] == "application/json"

    def test_map_records_response_with_orgs_wrapper(self):
        """Test mapping response with orgs wrapper."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()
            name = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "orgs"

        query = clearskies.query.Query(model_class=MockModel)
        response_data = {
            "orgs": [
                {"id": "org-1", "name": "Org One"},
                {"id": "org-2", "name": "Org Two"},
            ]
        }

        records = backend.map_records_response(response_data, query)
        assert len(records) == 2
        assert records[0]["id"] == "org-1"
        assert records[1]["name"] == "Org Two"

    def test_map_records_response_with_projects_wrapper(self):
        """Test mapping response with projects wrapper."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()
            name = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "projects"

        query = clearskies.query.Query(model_class=MockModel)
        response_data = {
            "projects": [
                {"id": "proj-1", "name": "Project One"},
            ]
        }

        records = backend.map_records_response(response_data, query)
        assert len(records) == 1
        assert records[0]["id"] == "proj-1"

    def test_map_records_response_with_single_record(self):
        """Test mapping response with a single record."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()
            name = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "org"

        query = clearskies.query.Query(model_class=MockModel)
        response_data = {"id": "org-1", "name": "Org One"}

        records = backend.map_records_response(response_data, query)
        assert len(records) == 1
        assert records[0]["id"] == "org-1"

    def test_map_records_response_with_list(self):
        """Test mapping response that is already a list."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()
            name = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "items"

        query = clearskies.query.Query(model_class=MockModel)
        response_data = [
            {"id": "item-1", "name": "Item One"},
            {"id": "item-2", "name": "Item Two"},
        ]

        records = backend.map_records_response(response_data, query)
        assert len(records) == 2

    def test_custom_base_url(self):
        """Test that a custom base URL can be set."""
        backend = SnykV1Backend(base_url="https://custom.snyk.io/v1/")
        assert backend.base_url == "https://custom.snyk.io/v1/"

    def test_pagination_adapter_is_snyk_v1(self):
        """Backend defaults to SnykV1PaginationAdapter."""
        from clearskies_snyk.backends.adapters import SnykV1PaginationAdapter

        backend = SnykV1Backend()
        assert isinstance(backend.pagination_adapter, SnykV1PaginationAdapter)
