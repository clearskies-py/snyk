"""Reference to SnykOrgAuditLog model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_audit_log import SnykOrgAuditLog


class SnykOrgAuditLogReference(ModelClassReference["SnykOrgAuditLog"]):
    """Reference to SnykOrgAuditLog model."""

    def get_model_class(self) -> type["SnykOrgAuditLog"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_audit_log

        return snyk_org_audit_log.SnykOrgAuditLog
