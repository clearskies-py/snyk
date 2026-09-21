"""Reference to SnykSlackChannel model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_slack_channel import SnykSlackChannel


class SnykSlackChannelReference(ModelClassReference["SnykSlackChannel"]):
    """Reference to SnykSlackChannel model."""

    def get_model_class(self) -> type["SnykSlackChannel"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_slack_channel

        return snyk_slack_channel.SnykSlackChannel
