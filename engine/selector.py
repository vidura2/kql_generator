"""Selection logic for detection and table candidates."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .scorer import best_scored_item, confidence_from_scores


def select_detection(
    user_input: str, detections: Dict[str, Any]
) -> Tuple[str, Dict[str, Any], float, List[str]]:
    """Select the best detection based on configured keywords."""
    detection_items = []
    for detection_name, payload in detections.items():
        keywords = payload.get("keywords", [])
        if isinstance(keywords, list):
            detection_items.append((detection_name, keywords))

    selected, score, matched, max_score = best_scored_item(user_input, detection_items)
    confidence = confidence_from_scores(score, max_score)

    if score <= 0 or not selected:
        return "", {}, 0.0, []
    return selected, detections[selected], confidence, matched


def select_table(
    user_input: str, tables: Dict[str, Any]
) -> Tuple[str, Dict[str, Any], float, List[str]]:
    """Select the best table when detection matching fails."""
    table_items = []
    for table_name, payload in tables.items():
        keywords = payload.get("keywords", [])
        if isinstance(keywords, list):
            table_items.append((table_name, keywords))

    selected, score, matched, max_score = best_scored_item(user_input, table_items)
    confidence = confidence_from_scores(score, max_score)

    if score <= 0 or not selected:
        return "", {}, 0.0, []
    return selected, tables[selected], confidence, matched
