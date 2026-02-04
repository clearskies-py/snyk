"""Tests for SnykOrgV1 model."""

from clearskies import Model

from clearskies_snyk.backends import SnykV1Backend
from clearskies_snyk.models.v1 import SnykOrgV1


class TestSnykOrgV1:
    """Test suite for SnykOrgV1 model."""

    def test_destination_name_returns_orgs(self) -> None:
        """Test that destination_name returns 'orgs' for v1 API."""
        assert SnykOrgV1.destination_name() == "orgs"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykOrgV1 has the expected columns."""
        assert hasattr(SnykOrgV1, "name")
        assert hasattr(SnykOrgV1, "slug")
        assert hasattr(SnykOrgV1, "url")
        assert hasattr(SnykOrgV1, "group")

    def test_model_inherits_from_clearskies_model(self) -> None:
        """Test that SnykOrgV1 inherits from clearskies.Model."""
        assert issubclass(SnykOrgV1, Model)

    def test_model_uses_snyk_v1_backend(self) -> None:
        """Test that SnykOrgV1 uses SnykV1Backend."""
        assert isinstance(SnykOrgV1.backend, SnykV1Backend)
