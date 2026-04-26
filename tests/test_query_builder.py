"""Unit tests for query builder."""

import unittest

from engine.query_builder import build_query_from_definition


class TestQueryBuilder(unittest.TestCase):
    def test_build_query_from_detection_definition(self) -> None:
        definition = {
            "table": "DeviceProcessEvents",
            "time_range": "1d",
            "filters": ["tolower(FileName) has \"powershell\""],
            "summarize": "Count=count() by DeviceName",
            "post_filters": ["Count >= 1"],
            "columns": ["Timestamp", "DeviceName", "Count"],
        }
        query = build_query_from_definition(definition, fallback_filters=[])

        self.assertIn("DeviceProcessEvents", query)
        self.assertIn("| where Timestamp >= ago(1d)", query)
        self.assertIn("| summarize Count=count() by DeviceName", query)
        self.assertIn("| order by Timestamp desc", query)
        self.assertIn("| limit 50", query)

    def test_build_query_applies_fallback_filters(self) -> None:
        definition = {
            "table": "DeviceNetworkEvents",
            "columns": ["Timestamp", "RemoteIP"],
        }
        query = build_query_from_definition(
            definition,
            fallback_filters=["not(ipv4_is_private(RemoteIP))"],
        )
        self.assertIn("| where not(ipv4_is_private(RemoteIP))", query)


if __name__ == "__main__":
    unittest.main()
