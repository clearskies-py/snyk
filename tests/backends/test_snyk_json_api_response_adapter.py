"""Tests for SnykJsonApiResponseAdapter."""

from __future__ import annotations

import pytest

from clearskies_snyk.backends.adapters import SnykJsonApiResponseAdapter


class TestSnykJsonApiResponseAdapter:
    """Unit tests for SnykJsonApiResponseAdapter."""

    def setup_method(self):
        self.adapter = SnykJsonApiResponseAdapter()

    # ------------------------------------------------------------------
    # extract_records
    # ------------------------------------------------------------------

    def test_extract_records_returns_flattened_list(self):
        """Data array is unwrapped and attributes promoted to top level."""
        response_data = {
            "data": [
                {"id": "org-1", "type": "org", "attributes": {"name": "Org One", "slug": "org-one"}},
                {"id": "org-2", "type": "org", "attributes": {"name": "Org Two", "slug": "org-two"}},
            ]
        }
        records = self.adapter.extract_records(response_data)
        assert records is not None
        assert len(records) == 2
        assert records[0]["id"] == "org-1"
        assert records[0]["name"] == "Org One"
        assert records[0]["slug"] == "org-one"
        assert records[1]["id"] == "org-2"

    def test_extract_records_returns_empty_list_for_empty_data(self):
        """Empty data array returns empty list (not None)."""
        records = self.adapter.extract_records({"data": []})
        assert records == []

    def test_extract_records_returns_none_for_non_dict(self):
        """Non-dict response falls through to ApiBackend logic."""
        assert self.adapter.extract_records("not a dict") is None
        assert self.adapter.extract_records([]) is None

    def test_extract_records_returns_none_without_data_key(self):
        """Response without a 'data' key returns None (pass-through to ApiBackend)."""
        assert self.adapter.extract_records({"orgs": []}) is None

    def test_extract_records_returns_empty_for_null_data(self):
        """data: null is treated as zero records (not an error)."""
        assert self.adapter.extract_records({"data": None}) == []

    def test_extract_records_wraps_single_record_dict(self):
        """Single-resource 'data' dict is wrapped in a list (for find() calls)."""
        response_data = {"data": {"id": "target-1", "type": "target", "attributes": {"display_name": "my-repo"}}}
        records = self.adapter.extract_records(response_data)
        assert records is not None
        assert len(records) == 1
        assert records[0]["id"] == "target-1"
        assert records[0]["display_name"] == "my-repo"

    # ------------------------------------------------------------------
    # extract_record
    # ------------------------------------------------------------------

    def test_extract_record_unwraps_single_data_object(self):
        """Single-resource 'data' object is unwrapped correctly."""
        response_data = {"data": {"id": "proj-1", "type": "project", "attributes": {"name": "My Project"}}}
        record = self.adapter.extract_record(response_data)
        assert record is not None
        assert record["id"] == "proj-1"
        assert record["name"] == "My Project"

    # ------------------------------------------------------------------
    # Relationship extraction
    # ------------------------------------------------------------------

    def test_relationship_ids_are_promoted(self):
        """Relationship data is extracted as {name}_id fields."""
        data_block = {
            "id": "proj-1",
            "type": "project",
            "attributes": {"name": "My Repo"},
            "relationships": {
                "target": {"data": {"id": "tgt-99", "type": "target"}},
            },
        }
        records = self.adapter.extract_records({"data": [data_block]})
        assert records is not None
        assert records[0]["target_id"] == "tgt-99"

    def test_organization_relationship_mapped_to_org_id(self):
        """'organization' relationship is mapped to 'org_id' (Snyk name convention)."""
        data_block = {
            "id": "proj-1",
            "type": "project",
            "attributes": {"name": "My Repo"},
            "relationships": {
                "organization": {"data": {"id": "org-abc", "type": "org"}},
            },
        }
        records = self.adapter.extract_records({"data": [data_block]})
        assert records is not None
        assert records[0]["org_id"] == "org-abc"
        assert "organization_id" not in records[0]

    def test_multiple_relationships_all_extracted(self):
        """Multiple relationships are all extracted as _id fields."""
        data_block = {
            "id": "proj-1",
            "type": "project",
            "attributes": {"name": "My Repo"},
            "relationships": {
                "organization": {"data": {"id": "org-abc", "type": "org"}},
                "target": {"data": {"id": "tgt-99", "type": "target"}},
            },
        }
        records = self.adapter.extract_records({"data": [data_block]})
        assert records is not None
        assert records[0]["org_id"] == "org-abc"
        assert records[0]["target_id"] == "tgt-99"

    def test_relationship_without_data_key_ignored(self):
        """Relationships missing an inner 'data' dict are skipped silently."""
        data_block = {
            "id": "proj-1",
            "type": "project",
            "attributes": {},
            "relationships": {
                "broken": {"links": {"related": "/some/url"}},
            },
        }
        records = self.adapter.extract_records({"data": [data_block]})
        assert records is not None
        assert "broken_id" not in records[0]

    def test_non_dict_relationship_value_ignored(self):
        """Non-dict relationship values are skipped gracefully."""
        data_block = {
            "id": "proj-1",
            "type": "project",
            "attributes": {},
            "relationships": {"weird": "not-a-dict"},
        }
        records = self.adapter.extract_records({"data": [data_block]})
        assert records is not None
        assert "weird_id" not in records[0]

    def test_record_without_relationships_key(self):
        """Records without a 'relationships' key are handled cleanly."""
        data_block = {"id": "org-1", "type": "org", "attributes": {"name": "My Org"}}
        records = self.adapter.extract_records({"data": [data_block]})
        assert records is not None
        assert records[0]["id"] == "org-1"

    # ------------------------------------------------------------------
    # Normalisation: id/type precedence
    # ------------------------------------------------------------------

    def test_root_id_takes_precedence_over_attribute_id(self):
        """Root-level 'id' wins over same-named field inside attributes."""
        data_block = {
            "id": "root-id",
            "type": "thing",
            "attributes": {"id": "attr-id", "name": "value"},
        }
        records = self.adapter.extract_records({"data": [data_block]})
        assert records is not None
        assert records[0]["id"] == "root-id"
