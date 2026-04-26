"""Unit tests for scorer utilities."""

import unittest

from engine.scorer import confidence_from_scores, score_keywords


class TestScorer(unittest.TestCase):
    def test_score_keywords_matches_multi_word_keyword(self) -> None:
        score, matches = score_keywords("show failed login burst", ["failed login", "powershell"])
        self.assertEqual(score, 1)
        self.assertEqual(matches, ["failed login"])

    def test_score_keywords_matches_substring(self) -> None:
        score, matches = score_keywords("find suspicious powershell", ["powershell", "pwsh"])
        self.assertEqual(score, 1)
        self.assertEqual(matches, ["powershell"])

    def test_confidence_from_scores(self) -> None:
        self.assertEqual(confidence_from_scores(2, 4), 0.5)
        self.assertEqual(confidence_from_scores(0, 3), 0.0)


if __name__ == "__main__":
    unittest.main()
