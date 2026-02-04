"""
Prompt templates for LLM-assisted test generation.

This module contains templates that can be used to generate high-quality
test cases by feeding API spec chunks to an LLM.

Usage:
    from tools.prompt_templates import MODEL_TEST_TEMPLATE, format_prompt
    
    prompt = format_prompt(
        MODEL_TEST_TEMPLATE,
        tag_name="Orgs",
        chunk_json=chunk_data,
        model_name="SnykOrg"
    )
"""

from __future__ import annotations

import json
from typing import Any


# =============================================================================
# Template: Model Unit Test Generation
# =============================================================================

MODEL_TEST_TEMPLATE = '''
# Context: Clearskies Snyk Model Test Generation

## Project Context
You are generating tests for the `clearskies-snyk` Python module, which provides 
ORM-like models for the Snyk REST API using the Clearskies framework.

## Existing Patterns
Models follow this pattern:
- Inherit from `clearskies.Model`
- Use `SnykBackend()` for API communication
- Define columns using `clearskies.columns` (String, Boolean, Datetime, Json, etc.)
- Implement `destination_name()` returning the API endpoint path
- Handle JSON:API format responses (data/attributes/relationships)

## Test Framework
- Use `pytest` with `unittest.mock`
- Mock the `requests` module or use `responses` library
- Follow existing test patterns in `tests/backends/test_snyk_backend.py`

## API Specification Chunk
The following is a subset of the Snyk REST API specification for the "{tag_name}" domain:

```json
{chunk_json}
```

## Shared Schemas Reference
These common schemas may be referenced:
```json
{common_schemas_json}
```

## Task
Generate comprehensive pytest tests for the `{model_name}` model that:

1. **Unit Tests**:
   - Test model initialization with valid data
   - Test column type validation
   - Test `destination_name()` returns correct endpoint
   - Test backend configuration

2. **Response Mapping Tests**:
   - Test `map_records_response()` correctly flattens JSON:API format
   - Test relationship ID extraction (e.g., `organization` → `org_id`)
   - Test handling of missing/null attributes

3. **Pagination Tests**:
   - Test `get_next_page_data_from_response()` extracts cursor
   - Test handling when no next page exists

4. **Edge Cases**:
   - Empty response handling
   - Single record vs list response
   - Invalid/malformed response handling

## Output Format
Provide complete, runnable pytest test code with:
- Proper imports
- Descriptive test names following `test_<what>_<condition>_<expected>` pattern
- Docstrings explaining each test
- Mock fixtures for API responses
- Assertions using native `assert` statements
'''


# =============================================================================
# Template: Schema Validation Test Generation
# =============================================================================

SCHEMA_VALIDATION_TEMPLATE = '''
# Context: Schema Validation Test Generation

## Task
Generate tests that validate the `{model_name}` model's columns match the 
OpenAPI schema definition.

## Schema Definition
```json
{schema_json}
```

## Model Definition
```python
{model_code}
```

## Requirements
1. Verify all required schema properties have corresponding model columns
2. Verify column types match schema types:
   - `string` → `String()`
   - `boolean` → `Boolean()`
   - `integer` → `Integer()`
   - `array` → `Json()` or custom column
   - `object` → `Json()`
   - `string` with `format: date-time` → `Datetime()`
   - `string` with `enum` → `Select(allowed_values=[...])`

3. Verify `is_searchable` columns match query parameters
4. Verify relationship columns match JSON:API relationships

## Output
Generate a test file that programmatically validates schema compliance.
'''


# =============================================================================
# Template: Integration Test Generation
# =============================================================================

INTEGRATION_TEST_TEMPLATE = '''
# Context: Integration Test Generation

## API Endpoint
```
{method} {path}
```

## Request/Response Specification
```json
{endpoint_spec_json}
```

## Task
Generate integration tests that:

1. **Happy Path**: Test successful API call with valid parameters
2. **Error Handling**: Test 400, 401, 403, 404, 500 responses
3. **Pagination**: Test cursor-based pagination if applicable
4. **Query Parameters**: Test filtering, sorting, limiting

## Constraints
- Use `responses` library for HTTP mocking
- Do NOT make actual API calls
- Validate request format matches spec
- Validate response handling matches spec

## Output
Complete pytest integration test with mocked HTTP responses.
'''


# =============================================================================
# Template: Model Implementation Generation
# =============================================================================

MODEL_IMPLEMENTATION_TEMPLATE = '''
# Context: Clearskies Snyk Model Implementation

## Task
Generate a new model class for the `{resource_name}` resource based on the 
OpenAPI specification.

## API Specification
```json
{spec_json}
```

## Existing Model Pattern
Follow this pattern from existing models:

```python
from typing import Self
from clearskies import Model
from clearskies.columns import Boolean, Datetime, Json, Select, String
from clearskies_snyk.backends import SnykBackend

class SnykExample(Model):
    """Model for Snyk Example resource."""
    
    id_column_name: str = "id"
    backend = SnykBackend()
    
    @classmethod
    def destination_name(cls: type[Self]) -> str:
        return "endpoint/path"
    
    id = String()
    name = String()
    # ... other columns
```

## Requirements
1. Use appropriate column types based on schema
2. Handle relationships using `{relationship}_id` pattern
3. Add `is_searchable=True` for query parameters
4. Add docstrings for the class and each column
5. Map API field names to Python-friendly names if needed (e.g., `type` → `resource_type`)

## Output
Complete model class implementation.
'''


# =============================================================================
# Helper Functions
# =============================================================================

def format_prompt(
    template: str,
    **kwargs: Any
) -> str:
    """
    Format a prompt template with the given parameters.
    
    Args:
        template: The prompt template string
        **kwargs: Parameters to substitute into the template
    
    Returns:
        Formatted prompt string
    """
    # Convert dict/list values to JSON strings
    formatted_kwargs = {}
    for key, value in kwargs.items():
        if isinstance(value, (dict, list)):
            formatted_kwargs[key] = json.dumps(value, indent=2)
        else:
            formatted_kwargs[key] = value
    
    return template.format(**formatted_kwargs)


def truncate_json(data: dict[str, Any], max_chars: int = 10000) -> str:
    """
    Truncate JSON data to fit within a character limit.
    
    Args:
        data: The data to serialize
        max_chars: Maximum characters allowed
    
    Returns:
        JSON string, possibly truncated
    """
    json_str = json.dumps(data, indent=2)
    if len(json_str) <= max_chars:
        return json_str
    
    # Truncate and add indicator
    return json_str[:max_chars - 50] + '\n\n... [TRUNCATED]'


def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a text string.
    
    Uses a rough approximation of 4 characters per token.
    
    Args:
        text: The text to estimate
    
    Returns:
        Estimated token count
    """
    return len(text) // 4


def create_model_test_prompt(
    chunk: dict[str, Any],
    common_schemas: dict[str, Any],
    model_name: str,
    max_tokens: int = 15000
) -> str:
    """
    Create a prompt for generating model tests.
    
    Args:
        chunk: The API spec chunk for this domain
        common_schemas: Common schemas shared across domains
        model_name: Name of the model class to test
        max_tokens: Maximum tokens for the prompt
    
    Returns:
        Formatted prompt string
    """
    # Truncate if needed
    chunk_json = truncate_json(chunk, max_chars=40000)
    schemas_json = truncate_json(common_schemas, max_chars=12000)
    
    prompt = format_prompt(
        MODEL_TEST_TEMPLATE,
        tag_name=chunk.get("tag", "Unknown"),
        chunk_json=chunk_json,
        common_schemas_json=schemas_json,
        model_name=model_name
    )
    
    # Check token estimate
    tokens = estimate_tokens(prompt)
    if tokens > max_tokens:
        # Further truncate chunk
        chunk_json = truncate_json(chunk, max_chars=20000)
        prompt = format_prompt(
            MODEL_TEST_TEMPLATE,
            tag_name=chunk.get("tag", "Unknown"),
            chunk_json=chunk_json,
            common_schemas_json=schemas_json,
            model_name=model_name
        )
    
    return prompt


def create_integration_test_prompt(
    method: str,
    path: str,
    endpoint_spec: dict[str, Any],
) -> str:
    """
    Create a prompt for generating integration tests.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        path: API endpoint path
        endpoint_spec: OpenAPI spec for this endpoint
    
    Returns:
        Formatted prompt string
    """
    return format_prompt(
        INTEGRATION_TEST_TEMPLATE,
        method=method,
        path=path,
        endpoint_spec_json=json.dumps(endpoint_spec, indent=2)
    )


# =============================================================================
# Model-to-Tag Mapping
# =============================================================================

MODEL_TAG_MAPPING = {
    "SnykOrg": "Orgs",
    "SnykGroup": "Groups",
    "SnykProject": "Projects",
    "SnykTarget": "Targets",
    "SnykCollection": "Collection",
    "SnykOrgIssue": "Issues",
    "SnykGroupIssue": "Issues",
    "SnykOrgServiceAccount": "ServiceAccounts",
    "SnykGroupServiceAccount": "ServiceAccounts",
    "SnykOrgMember": "Orgs",
    "SnykGroupMember": "Groups",
    "SnykGroupRole": "Groups",
    "SnykContainerImage": "ContainerImage",
    "SnykIntegration": "BrokerConnections",
}


def get_tag_for_model(model_name: str) -> str | None:
    """
    Get the API tag associated with a model.
    
    Args:
        model_name: Name of the model class
    
    Returns:
        Tag name or None if not found
    """
    return MODEL_TAG_MAPPING.get(model_name)
