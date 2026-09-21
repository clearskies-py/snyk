"""Reference to SnykBrokerDeployment model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_broker_deployment import SnykBrokerDeployment


class SnykBrokerDeploymentReference(ModelClassReference["SnykBrokerDeployment"]):
    """Reference to SnykBrokerDeployment model."""

    def get_model_class(self) -> type["SnykBrokerDeployment"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_broker_deployment

        return snyk_broker_deployment.SnykBrokerDeployment
