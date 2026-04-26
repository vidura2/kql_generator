"""Filter selection helpers."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .scorer import score_keywords


def select_filters(
    user_input: str,
    table_name: str,
    filters: Dict[str, Any],
) -> Tuple[List[str], List[str]]:
    """Select reusable filters based on keywords and table compatibility."""
    selected_expressions: List[str] = []
    matched_keywords: List[str] = []

    for _, filter_payload in filters.items():
        keywords = filter_payload.get("keywords", [])
        tables = filter_payload.get("tables", [])
        expression = filter_payload.get("expression", "")
        if (
            not isinstance(keywords, list)
            or not isinstance(tables, list)
            or not isinstance(expression, str)
        ):
            continue
        if table_name not in tables:
            continue

        score, matched = score_keywords(user_input, keywords)
        if score > 0:
            selected_expressions.append(expression)
            for keyword in matched:
                if keyword not in matched_keywords:
                    matched_keywords.append(keyword)

    return selected_expressions, matched_keywords
