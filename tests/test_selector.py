"""Unit tests for selector logic."""

import unittest

from engine.selector import select_detection, select_table


class TestSelector(unittest.TestCase):
    def test_select_detection_returns_best_match(self) -> None:
        detections = {
            "suspicious_powershell": {"keywords": ["powershell", "encoded"], "table": "DeviceProcessEvents"},
            "url_clicks": {"keywords": ["url click", "link"], "table": "UrlClickEvents"},
        }
        selected, payload, confidence, matched = select_detection("find suspicious powershell", detections)
        self.assertEqual(selected, "suspicious_powershell")
        self.assertEqual(payload["table"], "DeviceProcessEvents")
        self.assertGreater(confidence, 0)
        self.assertIn("powershell", matched)

    def test_select_table_returns_no_match_when_irrelevant(self) -> None:
        tables = {"DeviceProcessEvents": {"keywords": ["powershell", "cmd"], "columns": ["Timestamp"]}}
        selected, payload, confidence, matched = select_table("check unrelated astronomy", tables)
        self.assertEqual(selected, "")
        self.assertEqual(payload, {})
        self.assertEqual(confidence, 0.0)
        self.assertEqual(matched, [])


if __name__ == "__main__":
    unittest.main()
