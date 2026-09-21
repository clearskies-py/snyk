"""Reference to SnykBrokerConnection model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_broker_connection import SnykBrokerConnection


class SnykBrokerConnectionReference(ModelClassReference["SnykBrokerConnection"]):
    """Reference to SnykBrokerConnection model."""

    def get_model_class(self) -> type["SnykBrokerConnection"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_broker_connection

        return snyk_broker_connection.SnykBrokerConnection
