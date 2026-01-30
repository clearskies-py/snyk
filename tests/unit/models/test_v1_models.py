"""Tests for V1 models."""

from clearskies_snyk.backends import SnykV1Backend


class TestSnykWebhook:
    """Test suite for SnykWebhook model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykWebhook

        assert SnykWebhook.destination_name() == "org/{org_id}/webhooks"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykWebhook has the expected columns."""
        from clearskies_snyk.models.v1 import SnykWebhook

        assert hasattr(SnykWebhook, "id")
        assert hasattr(SnykWebhook, "org_id")
        assert hasattr(SnykWebhook, "url")
        assert hasattr(SnykWebhook, "secret")

    def test_model_uses_v1_backend(self) -> None:
        """Test that SnykWebhook uses SnykV1Backend."""
        from clearskies_snyk.models.v1 import SnykWebhook

        assert isinstance(SnykWebhook.backend, SnykV1Backend)


class TestSnykEntitlement:
    """Test suite for SnykEntitlement model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykEntitlement

        assert SnykEntitlement.destination_name() == "org/{org_id}/entitlements"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykEntitlement has the expected columns."""
        from clearskies_snyk.models.v1 import SnykEntitlement

        assert hasattr(SnykEntitlement, "name")
        assert hasattr(SnykEntitlement, "org_id")
        assert hasattr(SnykEntitlement, "value")

    def test_model_uses_v1_backend(self) -> None:
        """Test that SnykEntitlement uses SnykV1Backend."""
        from clearskies_snyk.models.v1 import SnykEntitlement

        assert isinstance(SnykEntitlement.backend, SnykV1Backend)


class TestSnykDependency:
    """Test suite for SnykDependency model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykDependency

        assert SnykDependency.destination_name() == "org/{org_id}/dependencies"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykDependency has the expected columns."""
        from clearskies_snyk.models.v1 import SnykDependency

        assert hasattr(SnykDependency, "id")
        assert hasattr(SnykDependency, "org_id")
        assert hasattr(SnykDependency, "name")
        assert hasattr(SnykDependency, "version")
        assert hasattr(SnykDependency, "latest_version")
        assert hasattr(SnykDependency, "issues_critical")
        assert hasattr(SnykDependency, "issues_high")
        assert hasattr(SnykDependency, "issues_medium")
        assert hasattr(SnykDependency, "issues_low")
        assert hasattr(SnykDependency, "licenses")

    def test_model_uses_v1_backend(self) -> None:
        """Test that SnykDependency uses SnykV1Backend."""
        from clearskies_snyk.models.v1 import SnykDependency

        assert isinstance(SnykDependency.backend, SnykV1Backend)


class TestSnykLicense:
    """Test suite for SnykLicense model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykLicense

        assert SnykLicense.destination_name() == "org/{org_id}/licenses"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykLicense has the expected columns."""
        from clearskies_snyk.models.v1 import SnykLicense

        assert hasattr(SnykLicense, "id")
        assert hasattr(SnykLicense, "org_id")
        assert hasattr(SnykLicense, "severity")
        assert hasattr(SnykLicense, "instructions")
        assert hasattr(SnykLicense, "dependencies")
        assert hasattr(SnykLicense, "projects")

    def test_model_uses_v1_backend(self) -> None:
        """Test that SnykLicense uses SnykV1Backend."""
        from clearskies_snyk.models.v1 import SnykLicense

        assert isinstance(SnykLicense.backend, SnykV1Backend)


class TestSnykImportJob:
    """Test suite for SnykImportJob model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykImportJob

        assert SnykImportJob.destination_name() == "org/{org_id}/integrations/{integration_id}/import"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykImportJob has the expected columns."""
        from clearskies_snyk.models.v1 import SnykImportJob

        assert hasattr(SnykImportJob, "id")
        assert hasattr(SnykImportJob, "org_id")
        assert hasattr(SnykImportJob, "integration_id")
        assert hasattr(SnykImportJob, "status")
        assert hasattr(SnykImportJob, "created")
        assert hasattr(SnykImportJob, "logs")

    def test_model_uses_v1_backend(self) -> None:
        """Test that SnykImportJob uses SnykV1Backend."""
        from clearskies_snyk.models.v1 import SnykImportJob

        assert isinstance(SnykImportJob.backend, SnykV1Backend)


class TestSnykGroupRoleV1:
    """Test suite for SnykGroupRoleV1 model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykGroupRoleV1

        assert SnykGroupRoleV1.destination_name() == "group/{group_id}/roles"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykGroupRoleV1 has the expected columns."""
        from clearskies_snyk.models.v1 import SnykGroupRoleV1

        assert hasattr(SnykGroupRoleV1, "public_id")
        assert hasattr(SnykGroupRoleV1, "group_id")
        assert hasattr(SnykGroupRoleV1, "name")
        assert hasattr(SnykGroupRoleV1, "description")
        assert hasattr(SnykGroupRoleV1, "created")
        assert hasattr(SnykGroupRoleV1, "modified")

    def test_model_uses_v1_backend(self) -> None:
        """Test that SnykGroupRoleV1 uses SnykV1Backend."""
        from clearskies_snyk.models.v1 import SnykGroupRoleV1

        assert isinstance(SnykGroupRoleV1.backend, SnykV1Backend)


class TestSnykGroupTag:
    """Test suite for SnykGroupTag model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykGroupTag

        assert SnykGroupTag.destination_name() == "group/{group_id}/tags"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykGroupTag has the expected columns."""
        from clearskies_snyk.models.v1 import SnykGroupTag

        assert hasattr(SnykGroupTag, "key")
        assert hasattr(SnykGroupTag, "group_id")
        assert hasattr(SnykGroupTag, "value")

    def test_model_uses_v1_backend(self) -> None:
        """Test that SnykGroupTag uses SnykV1Backend."""
        from clearskies_snyk.models.v1 import SnykGroupTag

        assert isinstance(SnykGroupTag.backend, SnykV1Backend)


class TestSnykGroupSettings:
    """Test suite for SnykGroupSettings model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykGroupSettings

        assert SnykGroupSettings.destination_name() == "group/{group_id}/settings"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykGroupSettings has the expected columns."""
        from clearskies_snyk.models.v1 import SnykGroupSettings

        assert hasattr(SnykGroupSettings, "group_id")
        assert hasattr(SnykGroupSettings, "session_length")
        assert hasattr(SnykGroupSettings, "request_access")
        assert hasattr(SnykGroupSettings, "request_access_enabled")

    def test_model_uses_v1_backend(self) -> None:
        """Test that SnykGroupSettings uses SnykV1Backend."""
        from clearskies_snyk.models.v1 import SnykGroupSettings

        assert isinstance(SnykGroupSettings.backend, SnykV1Backend)


class TestSnykIntegration:
    """Test suite for SnykIntegration model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykIntegration

        assert SnykIntegration.destination_name() == "org/{org_id}/integrations"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykIntegration has the expected columns."""
        from clearskies_snyk.models.v1 import SnykIntegration

        assert hasattr(SnykIntegration, "id")
        assert hasattr(SnykIntegration, "org_id")

    def test_model_uses_v1_backend(self) -> None:
        """Test that SnykIntegration uses SnykV1Backend."""
        from clearskies_snyk.models.v1 import SnykIntegration

        assert isinstance(SnykIntegration.backend, SnykV1Backend)
