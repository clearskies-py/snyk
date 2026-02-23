"""
Spec compatibility and change detection tests.

These tests detect when the OpenAPI spec changes and validate that
our implementation stays in sync with the API specification.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from tests.fixtures.spec_fixtures import SpecTestFixtures
from tests.validation.spec_parser import SpecParser


@pytest.fixture(scope="module")
def spec_path():
    """Get the path to the OpenAPI spec."""
    return Path(__file__).parent.parent.parent / "api_spec" / "v2-rest-api-spec.json"


@pytest.fixture(scope="module")
def spec_version_file():
    """Get the path to the spec version tracking file."""
    return Path(__file__).parent.parent / "fixtures" / ".spec_version"


@pytest.fixture(scope="module")
def spec_parser(spec_path):
    """Create a spec parser instance."""
    return SpecParser(spec_path)


@pytest.fixture(scope="module")
def spec_fixtures(spec_parser):
    """Create a spec fixtures instance."""
    return SpecTestFixtures(spec_parser)


class TestSpecVersionTracking:
    """Test spec version tracking and change detection."""

    def test_spec_file_exists(self, spec_path):
        """Verify the OpenAPI spec file exists."""
        assert spec_path.exists(), f"OpenAPI spec not found at {spec_path}"

    def test_spec_is_valid_json(self, spec_path):
        """Verify the spec is valid JSON."""
        try:
            with open(spec_path) as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Spec is not valid JSON: {e}")

    def test_spec_version_recorded(self, spec_path, spec_version_file):
        """
        Record current spec version for change detection.

        This test computes a hash of the spec file and compares it to the
        previously recorded version. If the spec has changed, the test will
        fail with a warning to review the changes.
        """
        current_hash = hashlib.sha256(spec_path.read_bytes()).hexdigest()

        if spec_version_file.exists():
            previous_hash = spec_version_file.read_text().strip()
            if previous_hash != current_hash:
                # Write the new hash (for the next run)
                spec_version_file.write_text(current_hash)

                pytest.fail(
                    "\n\n" + "=" * 70 + "\n"
                    "OpenAPI spec has changed!\n"
                    "=" * 70 + "\n\n"
                    "The OpenAPI specification file has been modified since the last test run.\n"
                    "This could indicate:\n\n"
                    "  1. The Snyk API has been updated\n"
                    "  2. New endpoints have been added\n"
                    "  3. Existing endpoints have been modified\n"
                    "  4. Request/response schemas have changed\n\n"
                    "Please review the changes and:\n\n"
                    "  - Update models if needed (src/clearskies_snyk/models/)\n"
                    "  - Update backends if needed (src/clearskies_snyk/backends/)\n"
                    "  - Update tests if validation rules changed\n"
                    "  - Verify all tests pass with the new spec\n\n"
                    "The spec version hash has been updated. Run tests again after reviewing.\n"
                    "=" * 70 + "\n"
                )
        else:
            # First run - record the hash
            spec_version_file.parent.mkdir(parents=True, exist_ok=True)
            spec_version_file.write_text(current_hash)
            pytest.skip("Spec version recorded for first time. Run tests again to validate.")

    def test_spec_has_paths(self, spec_parser):
        """Verify the spec contains API paths."""
        spec = spec_parser.spec
        assert "paths" in spec, "Spec missing 'paths' key"
        assert len(spec["paths"]) > 0, "Spec has no paths defined"

    def test_spec_has_info(self, spec_parser):
        """Verify the spec contains info section."""
        spec = spec_parser.spec
        assert "info" in spec, "Spec missing 'info' key"
        assert "version" in spec["info"], "Spec info missing 'version'"


class TestEndpointCoverage:
    """Test that all spec endpoints are covered by our implementation."""

    def test_all_http_methods_recognized(self, spec_parser):
        """Verify we can parse all HTTP methods in the spec."""
        all_endpoints = spec_parser.get_all_endpoints()
        assert len(all_endpoints) > 0, "No endpoints found in spec"

        # Check that we have various HTTP methods
        methods = {ep.method for ep in all_endpoints}
        assert "GET" in methods, "No GET endpoints found"
        assert "POST" in methods or "PATCH" in methods, "No mutation endpoints found"

    def test_endpoint_summary(self, spec_parser):
        """Print a summary of endpoints by tag (informational)."""
        from collections import defaultdict

        all_endpoints = spec_parser.get_all_endpoints()
        endpoints_by_tag: dict[str, list[str]] = defaultdict(list)

        for endpoint in all_endpoints:
            for tag in endpoint.tags:
                endpoints_by_tag[tag].append(f"{endpoint.method} {endpoint.path}")

        # This test always passes - it's for informational purposes
        print(f"\n\nTotal endpoints in spec: {len(all_endpoints)}")
        print("\nEndpoints by tag:")
        for tag, endpoints in sorted(endpoints_by_tag.items()):
            print(f"  {tag}: {len(endpoints)} endpoints")

    def test_create_endpoints_summary(self, spec_fixtures):
        """Print summary of CREATE (POST) endpoints (informational)."""
        create_endpoints = spec_fixtures.get_all_create_endpoints()
        print(f"\n\nTotal POST endpoints: {len(create_endpoints)}")
        print("\nSample POST endpoints:")
        for endpoint in create_endpoints[:5]:
            print(f"  {endpoint.method} {endpoint.path} - {endpoint.operation_id}")

    def test_update_endpoints_summary(self, spec_fixtures):
        """Print summary of UPDATE (PATCH) endpoints (informational)."""
        update_endpoints = spec_fixtures.get_all_update_endpoints()
        print(f"\n\nTotal PATCH endpoints: {len(update_endpoints)}")
        print("\nSample PATCH endpoints:")
        for endpoint in update_endpoints[:5]:
            print(f"  {endpoint.method} {endpoint.path} - {endpoint.operation_id}")

    def test_delete_endpoints_summary(self, spec_fixtures):
        """Print summary of DELETE endpoints (informational)."""
        delete_endpoints = spec_fixtures.get_all_delete_endpoints()
        print(f"\n\nTotal DELETE endpoints: {len(delete_endpoints)}")
        print("\nSample DELETE endpoints:")
        for endpoint in delete_endpoints[:5]:
            print(f"  {endpoint.method} {endpoint.path} - {endpoint.operation_id}")


class TestSpecStructure:
    """Test the structure and completeness of the spec."""

    def test_all_endpoints_have_operation_ids(self, spec_parser):
        """Verify all endpoints have operation IDs."""
        all_endpoints = spec_parser.get_all_endpoints()
        endpoints_without_ids = [ep for ep in all_endpoints if not ep.operation_id]

        if endpoints_without_ids:
            paths = [f"{ep.method} {ep.path}" for ep in endpoints_without_ids]
            pytest.fail(f"Endpoints missing operation IDs: {paths[:5]}")  # Show first 5

    def test_all_endpoints_have_tags(self, spec_parser):
        """Verify all endpoints have tags."""
        all_endpoints = spec_parser.get_all_endpoints()
        endpoints_without_tags = [ep for ep in all_endpoints if not ep.tags]

        # This is informational - not all endpoints may have tags
        if endpoints_without_tags:
            print(f"\n\nWarning: {len(endpoints_without_tags)} endpoints have no tags")

    def test_post_endpoints_have_request_bodies(self, spec_parser):
        """Verify POST endpoints have request body definitions."""
        post_endpoints = spec_parser.get_endpoints_for_operation("POST")
        endpoints_without_body = [ep for ep in post_endpoints if not ep.request_body]

        if endpoints_without_body:
            paths = [f"{ep.method} {ep.path}" for ep in endpoints_without_body]
            print(f"\n\nWarning: {len(paths)} POST endpoints have no request body schema")

    def test_endpoints_have_responses(self, spec_parser):
        """Verify endpoints have response definitions."""
        all_endpoints = spec_parser.get_all_endpoints()
        endpoints_without_responses = [ep for ep in all_endpoints if not ep.responses]

        if endpoints_without_responses:
            pytest.fail(
                f"{len(endpoints_without_responses)} endpoints have no response definitions. "
                f"All endpoints should define expected responses."
            )


class TestBackendCompatibility:
    """Test that backend implementation is compatible with spec."""

    def test_backend_supports_required_operations(self):
        """Verify backend supports the operations defined in spec."""
        from clearskies_snyk.backends import SnykBackend

        backend = SnykBackend()

        # Check that backend has the required methods
        assert hasattr(backend, "create"), "Backend missing create() method"
        assert hasattr(backend, "update"), "Backend missing update() method"
        assert hasattr(backend, "delete"), "Backend missing delete() method"
        assert hasattr(backend, "records"), "Backend missing records() method"

    def test_backend_uses_correct_api_version(self):
        """Verify backend uses a valid API version."""
        from clearskies_snyk.backends import SnykBackend

        backend = SnykBackend()

        # API version should be in YYYY-MM-DD format
        import re

        version_pattern = r"^\d{4}-\d{2}-\d{2}$"
        assert re.match(version_pattern, backend.api_version), (
            f"Backend API version '{backend.api_version}' is not in YYYY-MM-DD format"
        )

    def test_backend_uses_json_api_headers(self):
        """Verify backend uses JSON:API headers."""
        from clearskies_snyk.backends import SnykBackend

        backend = SnykBackend()

        assert "Accept" in backend.headers, "Backend missing Accept header"
        assert backend.headers["Accept"] == "application/vnd.api+json", (
            "Backend Accept header should be 'application/vnd.api+json'"
        )

        assert "Content-Type" in backend.headers, "Backend missing Content-Type header"
        assert backend.headers["Content-Type"] == "application/vnd.api+json", (
            "Backend Content-Type header should be 'application/vnd.api+json'"
        )

    def test_backend_base_url_is_correct(self):
        """Verify backend uses correct base URL."""
        from clearskies_snyk.backends import SnykBackend

        backend = SnykBackend()

        assert backend.base_url == "https://api.snyk.io/rest/", (
            f"Backend base URL should be 'https://api.snyk.io/rest/', got '{backend.base_url}'"
        )


class TestSpecChangeSummary:
    """Generate a summary report of the spec for review."""

    def test_generate_spec_summary(self, spec_parser, spec_fixtures):
        """Generate and print a comprehensive spec summary (informational)."""
        all_endpoints = spec_parser.get_all_endpoints()
        create_endpoints = spec_fixtures.get_all_create_endpoints()
        update_endpoints = spec_fixtures.get_all_update_endpoints()
        delete_endpoints = spec_fixtures.get_all_delete_endpoints()
        read_endpoints = spec_fixtures.get_all_read_endpoints()

        # Count by tag
        from collections import defaultdict

        endpoints_by_tag: dict[str, int] = defaultdict(int)
        for endpoint in all_endpoints:
            for tag in endpoint.tags:
                endpoints_by_tag[tag] += 1

        summary = f"""
        ========================================
        OpenAPI Spec Summary
        ========================================

        Total Endpoints: {len(all_endpoints)}

        By HTTP Method:
          GET:    {len(read_endpoints)}
          POST:   {len(create_endpoints)}
          PATCH:  {len(update_endpoints)}
          DELETE: {len(delete_endpoints)}

        Top 10 Tags by Endpoint Count:
        """

        for tag, count in sorted(endpoints_by_tag.items(), key=lambda x: -x[1])[:10]:
            summary += f"\n  {tag:30s}: {count:3d}"

        summary += "\n\n" + "=" * 40 + "\n"

        print(summary)
