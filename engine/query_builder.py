"""KQL query builder."""

from __future__ import annotations

from typing import Any, Dict, List


def build_query_from_definition(definition: Dict[str, Any], fallback_filters: List[str]) -> str:
    """Build a KQL query from a detection/table definition."""
    table = definition.get("table", "")
    if not table:
        raise ValueError("Query definition is missing required field: table")

    time_range = definition.get("time_range", "1d")
    columns = definition.get("columns", [])
    summarize = definition.get("summarize", "")
    post_filters = definition.get("post_filters", [])

    lines: List[str] = [table, f"| where Timestamp >= ago({time_range})"]

    for filter_expression in definition.get("filters", []):
        lines.append(f"| where {filter_expression}")

    for filter_expression in fallback_filters:
        lines.append(f"| where {filter_expression}")

    if summarize:
        lines.append(f"| summarize {summarize}")

    for post_filter in post_filters:
        lines.append(f"| where {post_filter}")

    if columns:
        lines.append(f"| project {', '.join(columns)}")

    lines.append("| order by Timestamp desc")
    lines.append("| limit 50")
    return "\n".join(lines)
