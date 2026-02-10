"""Default authentication provider for Snyk API."""

import clearskies


class DefaultSnykAuth(clearskies.di.AdditionalConfigAutoImport):
    """
    Default authentication provider for Snyk API.

    This class provides automatic configuration for Snyk API authentication using
    the clearskies dependency injection system. It is auto-imported when the clearskies_snyk
    package is used, making authentication configuration seamless.

    The authentication can be configured in two ways:

    1. **Secret Path (recommended for production)**: Set the `SNYK_AUTH_SECRET_PATH` environment
       variable to point to a secret manager path containing the API key.

    2. **Direct Environment Key**: Set the `SNYK_AUTH_KEY` environment variable directly
       with the Snyk API key.

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrg

    # The authentication is automatically configured via environment variables
    # Option 1: Using secret path
    # export SNYK_AUTH_SECRET_PATH=/path/to/secret

    # Option 2: Using direct key
    # export SNYK_AUTH_KEY=your-api-key

    # Then use models normally - auth is handled automatically
    orgs = SnykOrg()
    for org in orgs:
        print(org.name)
    ```
    """

    def provide_snyk_auth(self, environment: clearskies.Environment):
        """
        Provide the Snyk authentication configuration.

        Checks for `SNYK_AUTH_SECRET_PATH` first, falling back to `SNYK_AUTH_KEY`
        if not set. Returns a SecretBearer authentication instance configured for
        the Snyk API.

        Args:
            environment: The clearskies Environment instance for accessing env variables.

        Returns:
            A SecretBearer authentication instance configured for Snyk API.
        """
        secret_path = environment.get("SNYK_AUTH_SECRET_PATH", silent=True)
        if secret_path:
            return clearskies.authentication.SecretBearer(secret_key=secret_path, header_prefix="token ")
        return clearskies.authentication.SecretBearer(environment_key="SNYK_AUTH_KEY", header_prefix="token ")
