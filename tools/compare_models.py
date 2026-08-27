#!/usr/bin/env python3
"""
Compare all clearskies model files against the decomposed API spec chunks.

Reports missing attribute fields, missing query-param search fields, and
missing enum values for every model. Pagination / versioning params
(starting_after, ending_before, limit, version, …) are intentionally excluded
since those are handled by the backend, not the model.

Prerequisites:
    Run the spec decomposer first to generate the chunks:
        python tools/spec_decomposer.py

Usage:
    python tools/compare_models.py
"""

import ast
import json
from pathlib import Path

MODELS_DIR = Path("/Users/tom.nijboer/Projects/github.com/clearskies-py/snyk/src/clearskies_snyk/models")
CHUNKS_DIR = Path("/Users/tom.nijboer/Projects/github.com/clearskies-py/snyk/api_spec/decomposed/chunks")
PARAMS_FILE = Path(
    "/Users/tom.nijboer/Projects/github.com/clearskies-py/snyk/api_spec/decomposed/shared/common_parameters.json"
)
RAW_SPEC = Path("/Users/tom.nijboer/Projects/github.com/clearskies-py/snyk/api_spec/v2-rest-api-spec.json")

with open(PARAMS_FILE) as f:
    SHARED_PARAMS = json.load(f)["parameters"]

with open(RAW_SPEC) as f:
    RAW = json.load(f)

ALL_SCHEMAS = RAW["components"]["schemas"]

# Explicit model -> chunk slug(s) mapping
MODEL_TO_CHUNKS: dict[str, list[str]] = {
    "snyk_access_request": ["accessrequests"],
    "snyk_ai_bom": ["aibom"],
    "snyk_broker_connection": ["brokerconnections"],
    "snyk_broker_connection_integration": ["brokerconnections"],
    "snyk_broker_deployment": ["brokerdeployments"],
    "snyk_cloud_environment": ["cloud"],
    "snyk_cloud_resource": ["cloud"],
    "snyk_cloud_scan": ["cloud"],
    "snyk_collection": ["collection"],
    "snyk_collection_relationship_project": ["collection"],
    "snyk_container_image": ["containerimage"],
    "snyk_container_image_target_ref": ["containerimage"],
    "snyk_custom_base_image": ["custom_base_images"],
    "snyk_fix_pull_request": ["projects"],
    "snyk_group": ["groups"],
    "snyk_group_app_install": ["apps"],
    "snyk_group_audit_log": ["audit_logs"],
    "snyk_group_export": ["export"],
    "snyk_group_issue": ["issues"],
    "snyk_group_member": ["groups"],
    "snyk_group_membership": ["groups"],
    "snyk_group_org_membership": ["groups"],
    "snyk_group_policy": ["policies"],
    "snyk_group_service_account": ["serviceaccounts"],
    "snyk_group_settings_iac": ["iacsettings"],
    "snyk_group_sso_connection": ["groups"],
    "snyk_group_sso_connection_user": ["groups"],
    "snyk_group_user": ["groups"],
    "snyk_learn_assignment": ["learn_assignment"],
    "snyk_learn_catalog": ["catalog_resource"],
    "snyk_org": ["orgs"],
    "snyk_org_app": ["apps"],
    "snyk_org_app_bot": ["apps"],
    "snyk_org_app_install": ["apps"],
    "snyk_org_audit_log": ["audit_logs"],
    "snyk_org_export": ["export"],
    "snyk_org_invite": ["invites"],
    "snyk_org_issue": ["issues"],
    "snyk_org_member": ["orgs"],
    "snyk_org_membership": ["orgs"],
    "snyk_org_policy": ["policies"],
    "snyk_org_policy_event": ["policies"],
    "snyk_org_service_account": ["serviceaccounts"],
    "snyk_org_settings_iac": ["iacsettings"],
    "snyk_org_settings_open_source": ["opensourcesettings"],
    "snyk_org_settings_sast": ["sastsettings"],
    "snyk_org_user": ["orgs"],
    "snyk_package": ["package", "package_version"],
    "snyk_project": ["projects"],
    "snyk_project_history": ["projects"],
    "snyk_project_ignore": ["projects"],
    "snyk_project_sbom": ["sbom"],
    "snyk_pull_request_template": ["pull_request_templates"],
    "snyk_sbom_test": ["sbom"],
    "snyk_self": ["users"],
    "snyk_self_app": ["apps"],
    "snyk_self_app_session": ["apps"],
    "snyk_slack_channel": ["slacksettings", "slack"],
    "snyk_slack_default_notification_settings": ["slacksettings"],
    "snyk_slack_project_notification_settings": ["slacksettings"],
    "snyk_target": ["targets"],
    "snyk_tenant": ["tenants"],
    "snyk_tenant_membership": ["tenants"],
    "snyk_tenant_role": ["tenantrole"],
    "snyk_test_job": ["tests"],
}

# Fields to always ignore (pagination, versioning, meta — never model fields)
ALWAYS_SKIP = {
    "id",
    "type",
    "self",
    "links",
    "jsonapi",
    "meta",
    "data",
    "relationships",
    "next",
    "prev",
    "first",
    "last",
    "count",
    "total",
    "errors",
    # pagination params
    "starting_after",
    "ending_before",
    "limit",
    # version
    "version",
    # response envelope fields
    "attributes",
    "included",
}

# Known field renames (api name -> model field name)
FIELD_RENAMES = {
    "type": "issue_type",
}


def resolve_schema(s: dict) -> dict:
    if "$ref" in s:
        return ALL_SCHEMAS.get(s["$ref"].split("/")[-1], {})
    return s


def extract_const_list(node) -> list[str]:
    if isinstance(node, ast.List):
        return [e.value for e in node.elts if isinstance(e, ast.Constant)]
    return []


def extract_model_fields(filepath: Path) -> tuple[set[str], dict[str, list[str]]]:
    tree = ast.parse(filepath.read_text())
    fields: set[str] = set()
    select_values: dict[str, list[str]] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            fields.add(target.id)
                            if isinstance(item.value, ast.Call):
                                func = item.value.func
                                fname = (
                                    func.id
                                    if isinstance(func, ast.Name)
                                    else func.attr
                                    if isinstance(func, ast.Attribute)
                                    else ""
                                )
                                if fname == "Select":
                                    if item.value.args:
                                        vals = extract_const_list(item.value.args[0])
                                        if vals:
                                            select_values[target.id] = vals
                                    for kw in item.value.keywords:
                                        if kw.arg == "allowed_values":
                                            vals = extract_const_list(kw.value)
                                            if vals:
                                                select_values[target.id] = vals
    return fields, select_values


def load_chunks_for_slugs(slugs: list[str]) -> list[dict]:
    chunks = []
    for slug in slugs:
        # Load all parts
        matched = list(CHUNKS_DIR.glob(f"domain_{slug}.json")) + list(CHUNKS_DIR.glob(f"domain_{slug}_part*.json"))
        for f in sorted(matched):
            with open(f) as fh:
                chunks.append(json.load(fh))
    return chunks


def extract_spec_info(chunks: list[dict]) -> tuple[set[str], set[str], dict[str, list[str]]]:
    """Extract specification info from chunks.

    Returns: (attribute_fields, query_param_fields, enum_map).
    """
    attr_fields: set[str] = set()
    query_params: set[str] = set()
    enum_fields: dict[str, list[str]] = {}

    for chunk in chunks:
        # Attribute schemas
        for sname, schema in chunk.get("schemas", {}).items():
            if "Attributes" in sname:
                for pname, pschema in schema.get("properties", {}).items():
                    attr_fields.add(pname)
                    r = resolve_schema(pschema)
                    if "enum" in r:
                        enum_fields[pname] = r["enum"]

        # Query params from endpoints
        for ep in chunk.get("endpoints", []):
            for param in ep.get("details", {}).get("parameters", []):
                if "$ref" in param:
                    pkey = param["$ref"].split("/")[-1]
                    rp = SHARED_PARAMS.get(pkey, {})
                    if rp.get("in") == "query":
                        api_name = rp.get("name", "")
                        mname = api_name.replace(".", "_")
                        query_params.add(mname)
                        s = resolve_schema(rp.get("schema", {}))
                        if "enum" in s:
                            enum_fields[mname] = s["enum"]
                        elif "enum" in s.get("items", {}):
                            enum_fields[mname] = s["items"]["enum"]
                elif param.get("in") == "query":
                    api_name = param.get("name", "")
                    query_params.add(api_name.replace(".", "_"))

    return attr_fields, query_params, enum_fields


def get_raw_attributes_schema(model_name: str) -> tuple[set[str], dict[str, list[str]]]:
    """Try to find *Attributes schema from raw spec using model name."""
    tag = model_name.replace("snyk_", "").replace("_", " ").title().replace(" ", "")
    fields: set[str] = set()
    enums: dict[str, list[str]] = {}
    for suffix in ["Attributes"]:
        candidate = f"{tag}{suffix}"
        if candidate in ALL_SCHEMAS:
            for pname, pschema in ALL_SCHEMAS[candidate].get("properties", {}).items():
                fields.add(pname)
                r = resolve_schema(pschema)
                if "enum" in r:
                    enums[pname] = r["enum"]
            break
    return fields, enums


def compare_all() -> dict[str, dict[str, list[str] | dict[str, list[str]] | str]]:
    """Compare all models against spec and return compliance report."""
    results: dict[str, dict[str, list[str] | dict[str, list[str]] | str]] = {}

    for model_file in sorted(MODELS_DIR.glob("snyk_*.py")):
        name = model_file.stem
        slugs = MODEL_TO_CHUNKS.get(name)
        if slugs is None:
            results[name] = {"status": "unmapped"}
            continue

        chunks = load_chunks_for_slugs(slugs)
        if not chunks:
            results[name] = {"status": "no_chunks"}
            continue

        model_fields, model_selects = extract_model_fields(model_file)
        spec_attrs, spec_params, spec_enums = extract_spec_info(chunks)
        raw_attrs, raw_enums = get_raw_attributes_schema(name)
        spec_attrs.update(raw_attrs)
        spec_enums.update(raw_enums)

        all_spec = spec_attrs | spec_params
        missing = all_spec - model_fields - ALWAYS_SKIP - set(FIELD_RENAMES.keys())

        missing_enums: dict[str, list[str]] = {}
        for field, vals in spec_enums.items():
            mfield = FIELD_RENAMES.get(field, field)
            if mfield in model_selects:
                gap = set(vals) - set(model_selects[mfield])
                if gap:
                    missing_enums[mfield] = sorted(gap)

        if missing or missing_enums:
            results[name] = {
                "missing_fields": sorted(missing),
                "missing_enum_values": missing_enums,
            }
        else:
            results[name] = {"status": "ok"}

    return results


results = compare_all()

gaps = [(m, i) for m, i in results.items() if "missing_fields" in i or "missing_enum_values" in i]
ok_count = sum(1 for i in results.values() if i.get("status") == "ok")
unmapped = [m for m, i in results.items() if i.get("status") == "unmapped"]

print(f"OK: {ok_count}  |  Gaps: {len(gaps)}  |  Unmapped: {len(unmapped)}\n")

for model, info in gaps:
    print(f"{'=' * 60}")
    print(f"MODEL: {model}")
    if info.get("missing_fields"):
        print(f"  Missing fields    : {info['missing_fields']}")
    if info.get("missing_enum_values"):
        print(f"  Missing enum vals : {info['missing_enum_values']}")

if unmapped:
    print(f"\nUnmapped models: {unmapped}")
