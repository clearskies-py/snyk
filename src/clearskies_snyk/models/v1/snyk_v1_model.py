"""Base model for Snyk v1 API models."""

import clearskies

from clearskies_snyk.backends import SnykV1Backend


class SnykV1Model(clearskies.Model):
    """
    Base model for Snyk v1 API entities.

    This model provides common configuration for all Snyk v1 API models,
    including the backend configuration and common columns.

    ## Usage

    Extend this model to create specific Snyk v1 entity models:

    ```python
    from clearskies_snyk.models import SnykV1Model
    import clearskies


    class SnykOrgV1(SnykV1Model):
        @classmethod
        def destination_name(cls) -> str:
            return "orgs"

        name = clearskies.columns.String()
        slug = clearskies.columns.String()
    ```
    """

    id_column_name: str = "id"
    backend = SnykV1Backend()

    id = clearskies.columns.String()
