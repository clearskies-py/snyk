"""
Tests for the DefaultSnykAuth provider.

This module tests the DefaultSnykAuth class which provides
automatic authentication configuration for Snyk API.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from clearskies_snyk.defaults import DefaultSnykAuth


class TestDefaultSnykAuth:
    """Tests for DefaultSnykAuth provider."""

    def test_provide_snyk_auth_with_secret_path(self) -> None:
        """Test authentication with SNYK_AUTH_SECRET_PATH environment variable."""
        auth_provider = DefaultSnykAuth()
        mock_environment = MagicMock()
        mock_environment.get.side_effect = lambda key, *args: (
            "/path/to/secret" if key == "SNYK_AUTH_SECRET_PATH" else None
        )

        with patch("clearskies.authentication.SecretBearer") as mock_secret_bearer:
            mock_secret_bearer.return_value = MagicMock()
            result = auth_provider.provide_snyk_auth(mock_environment)

            mock_secret_bearer.assert_called_once_with(
                secret_key="/path/to/secret",
                header_prefix="token ",
            )

    def test_provide_snyk_auth_with_environment_key(self) -> None:
        """Test authentication with SNYK_AUTH_KEY environment variable."""
        auth_provider = DefaultSnykAuth()
        mock_environment = MagicMock()
        # Return None/empty for SNYK_AUTH_SECRET_PATH to trigger fallback
        mock_environment.get.side_effect = lambda key, *args: (
            None if key == "SNYK_AUTH_SECRET_PATH" else "test-api-key"
        )

        with patch("clearskies.authentication.SecretBearer") as mock_secret_bearer:
            mock_secret_bearer.return_value = MagicMock()
            result = auth_provider.provide_snyk_auth(mock_environment)

            mock_secret_bearer.assert_called_once_with(
                environment_key="SNYK_AUTH_KEY",
                header_prefix="token ",
            )

    def test_provide_snyk_auth_prefers_secret_path(self) -> None:
        """Test that SNYK_AUTH_SECRET_PATH takes precedence over SNYK_AUTH_KEY."""
        auth_provider = DefaultSnykAuth()
        mock_environment = MagicMock()
        # Both are set, but secret_path should be preferred
        mock_environment.get.side_effect = lambda key, *args: (
            "/path/to/secret" if key == "SNYK_AUTH_SECRET_PATH" else "test-api-key"
        )

        with patch("clearskies.authentication.SecretBearer") as mock_secret_bearer:
            mock_secret_bearer.return_value = MagicMock()
            result = auth_provider.provide_snyk_auth(mock_environment)

            # Should use secret_key, not environment_key
            mock_secret_bearer.assert_called_once_with(
                secret_key="/path/to/secret",
                header_prefix="token ",
            )

    def test_default_snyk_auth_is_additional_config_auto_import(self) -> None:
        """Test that DefaultSnykAuth inherits from AdditionalConfigAutoImport."""
        import clearskies

        assert issubclass(DefaultSnykAuth, clearskies.di.AdditionalConfigAutoImport)

    def test_provide_snyk_auth_method_exists(self) -> None:
        """Test that provide_snyk_auth method exists."""
        auth_provider = DefaultSnykAuth()
        assert hasattr(auth_provider, "provide_snyk_auth")
        assert callable(auth_provider.provide_snyk_auth)
