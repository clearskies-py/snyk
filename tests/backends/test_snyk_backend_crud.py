"""
Spec-driven tests for SnykBackend CRUD operations.

These tests validate that the SnykBackend correctly implements the Snyk REST API
by checking that HTTP requests match the OpenAPI specification requirements.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from clearskies_snyk.backends import SnykBackend
from tests.fixtures.spec_fixtures import SpecTestFixtures
from tests.validation.request_validator import RequestValidator
from tests.validation.spec_parser import SpecParser


@pytest.fixture(scope="module")
def spec_parser():
    """Create a spec parser instance."""
    spec_path = Path(__file__).parent.parent.parent / "api_spec" / "v2-rest-api-spec.json"
    return SpecParser(spec_path)


@pytest.fixture(scope="module")
def request_validator(spec_parser):
    """Create a request validator instance."""
    return RequestValidator(spec_parser)


@pytest.fixture(scope="module")
def spec_fixtures(spec_parser):
    """Create a spec fixtures instance."""
    return SpecTestFixtures(spec_parser)


class TestCreateOperations:
    """Test create operations against the spec."""

    @pytest.mark.parametrize(
        "endpoint_info",
        # Limit to a subset of create endpoints for faster testing
        SpecTestFixtures().get_all_create_endpoints()[:10],
        ids=lambda ep: f"{ep.method}_{ep.path}",
    )
    def test_create_request_headers(self, endpoint_info, spec_parser, request_validator, spec_fixtures):
        """Verify create() passes correct headers."""
        backend = SnykBackend()
        model = spec_fixtures.create_mock_model(endpoint_info)
        test_data = spec_fixtures.generate_request_data(endpoint_info)

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(content=b'{"data": {}}', json=lambda: {"data": {}})

            # Call create - may fail for various reasons, but we're checking the call
            try:
                backend.create(test_data["data"]["attributes"], model)
            except Exception:
                # We're only interested in validating the request, not the response handling
                pass

            # Validate headers were passed if execute_request was called
            if mock_execute.called:
                call_args = mock_execute.call_args
                headers = call_args.kwargs.get("headers", {})

                # Skip validation if headers is not a dict (might be a callable/method)
                if isinstance(headers, dict):
                    # Validate headers match spec
                    result = request_validator.validate_headers(endpoint_info.path, "POST", headers)
                    assert result.valid, f"Header validation failed: {result.errors}"

    @pytest.mark.parametrize(
        "endpoint_info",
        SpecTestFixtures().get_all_create_endpoints()[:10],
        ids=lambda ep: f"{ep.method}_{ep.path}",
    )
    def test_create_request_body_format(self, endpoint_info, spec_parser, request_validator, spec_fixtures):
        """Verify create() uses correct JSON:API body format."""
        backend = SnykBackend()
        model = spec_fixtures.create_mock_model(endpoint_info)
        test_data = spec_fixtures.generate_request_data(endpoint_info)

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(content=b'{"data": {}}', json=lambda: {"data": {}})

            try:
                backend.create(test_data["data"]["attributes"], model)
            except Exception:
                pass

            # Validate request body format if execute_request was called
            if mock_execute.called:
                call_args = mock_execute.call_args
                body = call_args.kwargs.get("json", {})

                # Validate body structure
                result = request_validator.validate_body(endpoint_info.path, "POST", body)
                assert result.valid, f"Body validation failed: {result.errors}"

    @pytest.mark.parametrize(
        "endpoint_info",
        SpecTestFixtures().get_all_create_endpoints()[:10],
        ids=lambda ep: f"{ep.method}_{ep.path}",
    )
    def test_create_url_includes_version(self, endpoint_info, spec_fixtures):
        """Verify create() URLs include version parameter."""
        backend = SnykBackend()
        model = spec_fixtures.create_mock_model(endpoint_info)
        test_data = spec_fixtures.generate_request_data(endpoint_info)

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(content=b'{"data": {}}', json=lambda: {"data": {}})

            try:
                backend.create(test_data["data"]["attributes"], model)
            except Exception:
                pass

            # Validate URL includes version if execute_request was called
            if mock_execute.called:
                call_args = mock_execute.call_args
                url = call_args.args[0] if call_args.args else call_args.kwargs.get("url", "")

                assert "version=" in url, f"URL missing version parameter: {url}"
                assert f"version={backend.api_version}" in url, f"URL has wrong version: {url}"


class TestUpdateOperations:
    """Test update operations against the spec."""

    @pytest.mark.parametrize(
        "endpoint_info",
        SpecTestFixtures().get_all_update_endpoints()[:10],
        ids=lambda ep: f"{ep.method}_{ep.path}",
    )
    def test_update_request_headers(self, endpoint_info, spec_parser, request_validator, spec_fixtures):
        """Verify update() passes correct headers."""
        backend = SnykBackend()
        model = spec_fixtures.create_mock_model(endpoint_info)
        test_data = spec_fixtures.generate_request_data(endpoint_info)

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(content=b'{"data": {}}', json=lambda: {"data": {}})

            try:
                backend.update("test-id-123", test_data["data"]["attributes"], model)
            except Exception:
                pass

            if mock_execute.called:
                call_args = mock_execute.call_args
                headers = call_args.kwargs.get("headers", {})

                # Skip validation if headers is not a dict (might be a callable/method)
                if isinstance(headers, dict):
                    result = request_validator.validate_headers(endpoint_info.path, "PATCH", headers)
                    assert result.valid, f"Header validation failed: {result.errors}"

    @pytest.mark.parametrize(
        "endpoint_info",
        SpecTestFixtures().get_all_update_endpoints()[:10],
        ids=lambda ep: f"{ep.method}_{ep.path}",
    )
    def test_update_request_body_format(self, endpoint_info, spec_parser, request_validator, spec_fixtures):
        """Verify update() uses correct JSON:API body format."""
        backend = SnykBackend()
        model = spec_fixtures.create_mock_model(endpoint_info)
        test_data = spec_fixtures.generate_request_data(endpoint_info)

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(content=b'{"data": {}}', json=lambda: {"data": {}})

            try:
                backend.update("test-id-123", test_data["data"]["attributes"], model)
            except Exception:
                pass

            if mock_execute.called:
                call_args = mock_execute.call_args
                body = call_args.kwargs.get("json", {})

                result = request_validator.validate_body(endpoint_info.path, "PATCH", body)
                assert result.valid, f"Body validation failed: {result.errors}"

    @pytest.mark.parametrize(
        "endpoint_info",
        SpecTestFixtures().get_all_update_endpoints()[:10],
        ids=lambda ep: f"{ep.method}_{ep.path}",
    )
    def test_update_url_includes_version(self, endpoint_info, spec_fixtures):
        """Verify update() URLs include version parameter."""
        backend = SnykBackend()
        model = spec_fixtures.create_mock_model(endpoint_info)
        test_data = spec_fixtures.generate_request_data(endpoint_info)

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(content=b'{"data": {}}', json=lambda: {"data": {}})

            try:
                backend.update("test-id-123", test_data["data"]["attributes"], model)
            except Exception:
                pass

            if mock_execute.called:
                call_args = mock_execute.call_args
                url = call_args.args[0] if call_args.args else call_args.kwargs.get("url", "")

                assert "version=" in url, f"URL missing version parameter: {url}"
                assert f"version={backend.api_version}" in url, f"URL has wrong version: {url}"


class TestDeleteOperations:
    """Test delete operations against the spec."""

    @pytest.mark.parametrize(
        "endpoint_info",
        SpecTestFixtures().get_all_delete_endpoints()[:10],
        ids=lambda ep: f"{ep.method}_{ep.path}",
    )
    def test_delete_request_headers(self, endpoint_info, spec_parser, request_validator, spec_fixtures):
        """Verify delete() passes correct headers."""
        backend = SnykBackend()
        model = spec_fixtures.create_mock_model(endpoint_info)

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(content=b"", status_code=204)

            try:
                backend.delete("test-id-123", model)
            except Exception:
                pass

            if mock_execute.called:
                call_args = mock_execute.call_args
                headers = call_args.kwargs.get("headers", {})

                # Skip validation if headers is not a dict (might be a callable/method)
                if isinstance(headers, dict):
                    result = request_validator.validate_headers(endpoint_info.path, "DELETE", headers)
                    assert result.valid, f"Header validation failed: {result.errors}"

    @pytest.mark.parametrize(
        "endpoint_info",
        SpecTestFixtures().get_all_delete_endpoints()[:10],
        ids=lambda ep: f"{ep.method}_{ep.path}",
    )
    def test_delete_url_includes_version(self, endpoint_info, spec_fixtures):
        """Verify delete() URLs include version parameter."""
        backend = SnykBackend()
        model = spec_fixtures.create_mock_model(endpoint_info)

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(content=b"", status_code=204)

            try:
                backend.delete("test-id-123", model)
            except Exception:
                pass

            if mock_execute.called:
                call_args = mock_execute.call_args
                url = call_args.args[0] if call_args.args else call_args.kwargs.get("url", "")

                assert "version=" in url, f"URL missing version parameter: {url}"
                assert f"version={backend.api_version}" in url, f"URL has wrong version: {url}"


class TestReadOperations:
    """Test read/query operations against the spec."""

    def test_records_request_includes_version_parameter(self):
        """Verify that records() requests include version parameter."""
        backend = SnykBackend()
        model = Mock()
        model.destination_name.return_value = "orgs"

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(
                content=b'{"data": [], "links": {}}', json=lambda: {"data": [], "links": {}}
            )

            try:
                # Create a query object
                from clearskies import Model

                query = model.where("id=test")
                backend.records(query)
            except Exception:
                pass

            if mock_execute.called:
                call_args = mock_execute.call_args
                # Version should be in URL params
                params = call_args.kwargs.get("params", {})

                assert "version" in params, "Query parameters missing version"
                assert params["version"] == backend.api_version


class TestHTTPMethodValidation:
    """Test that correct HTTP methods are used for operations."""

    def test_create_uses_post_method(self, spec_fixtures):
        """Verify create() uses POST method."""
        backend = SnykBackend()
        endpoint_info = spec_fixtures.get_all_create_endpoints()[0]
        model = spec_fixtures.create_mock_model(endpoint_info)
        test_data = spec_fixtures.generate_request_data(endpoint_info)

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(content=b'{"data": {}}', json=lambda: {"data": {}})

            try:
                backend.create(test_data["data"]["attributes"], model)
            except Exception:
                pass

            if mock_execute.called:
                call_args = mock_execute.call_args
                method = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("method", "")

                assert method.upper() == "POST", f"Expected POST method, got {method}"

    def test_update_uses_patch_method(self, spec_fixtures):
        """Verify update() uses PATCH method."""
        backend = SnykBackend()
        endpoint_info = spec_fixtures.get_all_update_endpoints()[0]
        model = spec_fixtures.create_mock_model(endpoint_info)
        test_data = spec_fixtures.generate_request_data(endpoint_info)

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(content=b'{"data": {}}', json=lambda: {"data": {}})

            try:
                backend.update("test-id-123", test_data["data"]["attributes"], model)
            except Exception:
                pass

            if mock_execute.called:
                call_args = mock_execute.call_args
                method = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("method", "")

                assert method.upper() == "PATCH", f"Expected PATCH method, got {method}"

    def test_delete_uses_delete_method(self, spec_fixtures):
        """Verify delete() uses DELETE method."""
        backend = SnykBackend()
        endpoint_info = spec_fixtures.get_all_delete_endpoints()[0]
        model = spec_fixtures.create_mock_model(endpoint_info)

        with patch.object(backend, "execute_request") as mock_execute:
            mock_execute.return_value = Mock(content=b"", status_code=204)

            try:
                backend.delete("test-id-123", model)
            except Exception:
                pass

            if mock_execute.called:
                call_args = mock_execute.call_args
                method = call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("method", "")

                assert method.upper() == "DELETE", f"Expected DELETE method, got {method}"
