"""Base model for Snyk API integration."""

from clearskies import Model

from clearskies_snyk.backends import SnykBackend


class SnykModel(Model):
    """
    Base model for Snyk API integration.

    This is the foundational model class for all Snyk-related models. It pre-configures
    the SnykBackend for API communication with the Snyk platform.

    Extend this class to create models that interact with the Snyk API:

    ```python
    from clearskies_snyk.models import SnykModel
    from clearskies.columns import String, Boolean


    class MyCustomSnykModel(SnykModel):
        id_column_name = "id"

        id = String()
        name = String()
        is_active = Boolean()

        @classmethod
        def destination_name(cls):
            return "my-endpoint"
    ```
    """

    backend = SnykBackend()
