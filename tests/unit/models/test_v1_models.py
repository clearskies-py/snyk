"""Tests for V1 models."""

from clearskies_snyk.backends import SnykV1Backend, SnykV1ImportBackend


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

        assert hasattr(SnykImportJob, "job_id")
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


class TestSnykGitHubImport:
    """Test suite for SnykGitHubImport model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykGitHubImport

        assert SnykGitHubImport.destination_name() == "org/{org_id}/integrations/{integration_id}/import"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykGitHubImport has the expected columns."""
        from clearskies_snyk.models.v1 import SnykGitHubImport

        assert hasattr(SnykGitHubImport, "org_id")
        assert hasattr(SnykGitHubImport, "integration_id")
        assert hasattr(SnykGitHubImport, "target")
        assert hasattr(SnykGitHubImport, "files")
        assert hasattr(SnykGitHubImport, "exclusion_globs")

    def test_model_uses_v1_import_backend(self) -> None:
        """Test that SnykGitHubImport uses SnykV1ImportBackend."""
        from clearskies_snyk.models.v1 import SnykGitHubImport

        assert isinstance(SnykGitHubImport.backend, SnykV1ImportBackend)


class TestSnykGitLabImport:
    """Test suite for SnykGitLabImport model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykGitLabImport

        assert SnykGitLabImport.destination_name() == "org/{org_id}/integrations/{integration_id}/import"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykGitLabImport has the expected columns."""
        from clearskies_snyk.models.v1 import SnykGitLabImport

        assert hasattr(SnykGitLabImport, "org_id")
        assert hasattr(SnykGitLabImport, "integration_id")
        assert hasattr(SnykGitLabImport, "target")
        assert hasattr(SnykGitLabImport, "files")
        assert hasattr(SnykGitLabImport, "exclusion_globs")

    def test_model_uses_v1_import_backend(self) -> None:
        """Test that SnykGitLabImport uses SnykV1ImportBackend."""
        from clearskies_snyk.models.v1 import SnykGitLabImport

        assert isinstance(SnykGitLabImport.backend, SnykV1ImportBackend)


class TestSnykBitbucketCloudImport:
    """Test suite for SnykBitbucketCloudImport model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykBitbucketCloudImport

        assert SnykBitbucketCloudImport.destination_name() == "org/{org_id}/integrations/{integration_id}/import"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykBitbucketCloudImport has the expected columns."""
        from clearskies_snyk.models.v1 import SnykBitbucketCloudImport

        assert hasattr(SnykBitbucketCloudImport, "org_id")
        assert hasattr(SnykBitbucketCloudImport, "integration_id")
        assert hasattr(SnykBitbucketCloudImport, "target")
        assert hasattr(SnykBitbucketCloudImport, "files")
        assert hasattr(SnykBitbucketCloudImport, "exclusion_globs")

    def test_model_uses_v1_import_backend(self) -> None:
        """Test that SnykBitbucketCloudImport uses SnykV1ImportBackend."""
        from clearskies_snyk.models.v1 import SnykBitbucketCloudImport

        assert isinstance(SnykBitbucketCloudImport.backend, SnykV1ImportBackend)


class TestSnykBitbucketServerImport:
    """Test suite for SnykBitbucketServerImport model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykBitbucketServerImport

        assert SnykBitbucketServerImport.destination_name() == "org/{org_id}/integrations/{integration_id}/import"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykBitbucketServerImport has the expected columns."""
        from clearskies_snyk.models.v1 import SnykBitbucketServerImport

        assert hasattr(SnykBitbucketServerImport, "org_id")
        assert hasattr(SnykBitbucketServerImport, "integration_id")
        assert hasattr(SnykBitbucketServerImport, "target")
        assert hasattr(SnykBitbucketServerImport, "files")
        assert hasattr(SnykBitbucketServerImport, "exclusion_globs")

    def test_model_uses_v1_import_backend(self) -> None:
        """Test that SnykBitbucketServerImport uses SnykV1ImportBackend."""
        from clearskies_snyk.models.v1 import SnykBitbucketServerImport

        assert isinstance(SnykBitbucketServerImport.backend, SnykV1ImportBackend)


class TestSnykAzureReposImport:
    """Test suite for SnykAzureReposImport model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykAzureReposImport

        assert SnykAzureReposImport.destination_name() == "org/{org_id}/integrations/{integration_id}/import"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykAzureReposImport has the expected columns."""
        from clearskies_snyk.models.v1 import SnykAzureReposImport

        assert hasattr(SnykAzureReposImport, "org_id")
        assert hasattr(SnykAzureReposImport, "integration_id")
        assert hasattr(SnykAzureReposImport, "target")
        assert hasattr(SnykAzureReposImport, "files")
        assert hasattr(SnykAzureReposImport, "exclusion_globs")

    def test_model_uses_v1_import_backend(self) -> None:
        """Test that SnykAzureReposImport uses SnykV1ImportBackend."""
        from clearskies_snyk.models.v1 import SnykAzureReposImport

        assert isinstance(SnykAzureReposImport.backend, SnykV1ImportBackend)


class TestSnykDockerHubImport:
    """Test suite for SnykDockerHubImport model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykDockerHubImport

        assert SnykDockerHubImport.destination_name() == "org/{org_id}/integrations/{integration_id}/import"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykDockerHubImport has the expected columns."""
        from clearskies_snyk.models.v1 import SnykDockerHubImport

        assert hasattr(SnykDockerHubImport, "org_id")
        assert hasattr(SnykDockerHubImport, "integration_id")
        assert hasattr(SnykDockerHubImport, "target")

    def test_model_uses_v1_import_backend(self) -> None:
        """Test that SnykDockerHubImport uses SnykV1ImportBackend."""
        from clearskies_snyk.models.v1 import SnykDockerHubImport

        assert isinstance(SnykDockerHubImport.backend, SnykV1ImportBackend)


class TestSnykContainerRegistryImport:
    """Test suite for SnykContainerRegistryImport model."""

    def test_destination_name_returns_correct_path(self) -> None:
        """Test that destination_name returns the correct v1 API path."""
        from clearskies_snyk.models.v1 import SnykContainerRegistryImport

        assert SnykContainerRegistryImport.destination_name() == "org/{org_id}/integrations/{integration_id}/import"

    def test_model_has_expected_columns(self) -> None:
        """Test that SnykContainerRegistryImport has the expected columns."""
        from clearskies_snyk.models.v1 import SnykContainerRegistryImport

        assert hasattr(SnykContainerRegistryImport, "org_id")
        assert hasattr(SnykContainerRegistryImport, "integration_id")
        assert hasattr(SnykContainerRegistryImport, "target")

    def test_model_uses_v1_import_backend(self) -> None:
        """Test that SnykContainerRegistryImport uses SnykV1ImportBackend."""
        from clearskies_snyk.models.v1 import SnykContainerRegistryImport

        assert isinstance(SnykContainerRegistryImport.backend, SnykV1ImportBackend)
