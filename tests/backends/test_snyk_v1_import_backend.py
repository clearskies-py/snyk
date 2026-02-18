"""Tests for SnykV1ImportBackend."""

from unittest.mock import MagicMock

import clearskies
import pytest

from clearskies_snyk.backends import SnykV1ImportBackend


class TestSnykV1ImportBackend:
    """Tests for the SnykV1ImportBackend class."""

    def test_inherits_from_snykv1backend(self):
        """Test that SnykV1ImportBackend inherits from SnykV1Backend."""
        from clearskies_snyk.backends import SnykV1Backend

        backend = SnykV1ImportBackend()
        assert isinstance(backend, SnykV1Backend)

    def test_create_extracts_job_id_from_location_header(self):
        """Test that create() extracts job ID from Location header."""
        test_backend = SnykV1ImportBackend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            backend = test_backend
            id = clearskies.columns.String()
            org_id = clearskies.columns.String()
            integration_id = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "org/{org_id}/integrations/{integration_id}/import"

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b""
        mock_response.headers = {
            "Location": "https://api.snyk.io/v1/org/4a18d42f-0706-4ad0-b127-24078731fbed/integrations/9a3e5d90-b782-468a-a042-9a2073736f0b/import/abc-123-def"
        }

        # Mock the execute_request method
        test_backend.execute_request = MagicMock(return_value=mock_response)

        model = MockModel()
        result = test_backend.create(
            {
                "org_id": "4a18d42f-0706-4ad0-b127-24078731fbed",
                "integration_id": "9a3e5d90-b782-468a-a042-9a2073736f0b",
                "target": {"owner": "myorg", "name": "myrepo", "branch": "main"},
            },
            model,
        )

        assert result.record["job_id"] == "abc-123-def"
        assert result.record["org_id"] == "4a18d42f-0706-4ad0-b127-24078731fbed"
        assert result.record["integration_id"] == "9a3e5d90-b782-468a-a042-9a2073736f0b"

    def test_create_extracts_job_id_from_relative_location(self):
        """Test that create() extracts job ID from relative Location header."""
        test_backend = SnykV1ImportBackend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            backend = test_backend
            id = clearskies.columns.String()
            org_id = clearskies.columns.String()
            integration_id = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "org/{org_id}/integrations/{integration_id}/import"

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b""
        mock_response.headers = {"Location": "/v1/org/org-123/integrations/int-456/import/job-789"}

        test_backend.execute_request = MagicMock(return_value=mock_response)

        model = MockModel()
        result = test_backend.create(
            {
                "org_id": "org-123",
                "integration_id": "int-456",
            },
            model,
        )

        assert result.record["job_id"] == "job-789"
        assert result.record["org_id"] == "org-123"
        assert result.record["integration_id"] == "int-456"

    def test_create_raises_error_on_malformed_location(self):
        """Test that create() raises ValueError on malformed Location header."""
        test_backend = SnykV1ImportBackend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            backend = test_backend
            id = clearskies.columns.String()
            org_id = clearskies.columns.String()
            integration_id = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "org/{org_id}/integrations/{integration_id}/import"

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b""
        mock_response.headers = {"Location": "/invalid/path/format"}

        test_backend.execute_request = MagicMock(return_value=mock_response)

        model = MockModel()
        with pytest.raises(ValueError, match="Could not extract job ID from Location header"):
            test_backend.create({"org_id": "org-123", "integration_id": "int-456"}, model)

    def test_create_handles_missing_import_segment(self):
        """Test that create() raises error when 'import' segment is missing."""
        test_backend = SnykV1ImportBackend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            backend = test_backend
            id = clearskies.columns.String()
            org_id = clearskies.columns.String()
            integration_id = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "org/{org_id}/integrations/{integration_id}/import"

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b""
        mock_response.headers = {"Location": "/v1/org/org-123/integrations/int-456"}

        test_backend.execute_request = MagicMock(return_value=mock_response)

        model = MockModel()
        with pytest.raises(ValueError, match="Could not extract job ID"):
            test_backend.create({"org_id": "org-123", "integration_id": "int-456"}, model)

    def test_create_handles_trailing_slash(self):
        """Test that create() handles Location header with trailing slash."""
        test_backend = SnykV1ImportBackend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            backend = test_backend
            id = clearskies.columns.String()
            org_id = clearskies.columns.String()
            integration_id = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "org/{org_id}/integrations/{integration_id}/import"

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b""
        mock_response.headers = {"Location": "/v1/org/org-123/integrations/int-456/import/job-789/"}

        test_backend.execute_request = MagicMock(return_value=mock_response)

        model = MockModel()
        result = test_backend.create({"org_id": "org-123", "integration_id": "int-456"}, model)

        assert result.record["job_id"] == "job-789"

    def test_create_raises_error_when_no_location_header(self):
        """Test that create() raises ValueError when no Location header is provided."""
        test_backend = SnykV1ImportBackend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            backend = test_backend
            id = clearskies.columns.String()
            org_id = clearskies.columns.String()
            integration_id = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "org/{org_id}/integrations/{integration_id}/import"

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b""
        mock_response.text = ""
        mock_response.headers = {}  # No Location header

        test_backend.execute_request = MagicMock(return_value=mock_response)

        model = MockModel()
        with pytest.raises(
            ValueError,
            match="Snyk API import endpoint returned no Location header. According to API specification",
        ):
            test_backend.create({"org_id": "org-123", "integration_id": "int-456"}, model)
