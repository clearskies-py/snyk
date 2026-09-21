"""Reference to SnykGroupAuditLog model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_audit_log import SnykGroupAuditLog


class SnykGroupAuditLogReference(ModelClassReference["SnykGroupAuditLog"]):
    """Reference to SnykGroupAuditLog model."""

    def get_model_class(self) -> type["SnykGroupAuditLog"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_audit_log

        return snyk_group_audit_log.SnykGroupAuditLog
