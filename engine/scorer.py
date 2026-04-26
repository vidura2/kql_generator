"""Keyword scoring helpers."""

from __future__ import annotations

import re
from typing import Iterable, List, Sequence, Tuple


def tokenize_text(text: str) -> List[str]:
    """Convert free-form input into lowercase tokens."""
    return re.findall(r"[a-z0-9_]+", text.lower())


def score_keywords(user_input: str, keywords: Sequence[str]) -> Tuple[int, List[str]]:
    """Return a match score and matched keywords based on substring + token matching."""
    normalized_input = user_input.lower()
    input_tokens = set(tokenize_text(user_input))

    score = 0
    matched: List[str] = []
    for keyword in keywords:
        keyword_lower = keyword.lower()
        keyword_tokens = set(tokenize_text(keyword_lower))
        if not keyword_tokens:
            continue

        # Match if all keyword tokens are present, or if keyword is a direct substring.
        token_match = keyword_tokens.issubset(input_tokens)
        substring_match = keyword_lower in normalized_input
        if token_match or substring_match:
            score += 1
            matched.append(keyword)
    return score, matched


def confidence_from_scores(selected_score: int, max_score: int) -> float:
    """Build a normalized confidence score from selected and maximum possible scores."""
    if max_score <= 0 or selected_score <= 0:
        return 0.0
    return round(selected_score / max_score, 3)


def best_scored_item(
    user_input: str,
    items: Iterable[Tuple[str, Sequence[str]]],
) -> Tuple[str, int, List[str], int]:
    """Find the highest-scoring item.

    Returns:
        tuple: (selected_name, score, matched_keywords, max_possible_score)
    """
    best_name = ""
    best_score = 0
    best_matches: List[str] = []
    best_max = 0

    for name, keywords in items:
        score, matches = score_keywords(user_input, keywords)
        max_possible = len(keywords)
        if score > best_score:
            best_name = name
            best_score = score
            best_matches = matches
            best_max = max_possible
    return best_name, best_score, best_matches, best_max
