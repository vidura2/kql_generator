"""Interactive CLI for internal KQL query generation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

from config_loader import ConfigLoadError, load_all_configs
from engine.filter_engine import select_filters
from engine.query_builder import build_query_from_definition
from engine.selector import select_detection, select_table


def generate_kql(user_input: str, configs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Generate KQL output dictionary from user input and configs."""
    detections = configs["detections"]
    tables = configs["tables"]
    filters = configs["filters"]

    detection_name, detection_payload, confidence, matched_keywords = select_detection(
        user_input, detections
    )
    if detection_name:
        query = build_query_from_definition(detection_payload, fallback_filters=[])
        return {
            "input": user_input,
            "mode": "detection",
            "selected_name": detection_name,
            "table": detection_payload.get("table", ""),
            "confidence": confidence,
            "matched_keywords": matched_keywords,
            "filters": detection_payload.get("filters", []),
            "query": query,
        }

    table_name, table_payload, table_confidence, table_keywords = select_table(user_input, tables)
    if not table_name:
        raise ValueError("No matching detection or table found for input.")

    matched_filters, filter_keywords = select_filters(user_input, table_name, filters)
    table_definition: Dict[str, Any] = {
        "table": table_name,
        "time_range": "1d",
        "filters": [],
        "summarize": "",
        "post_filters": [],
        "columns": table_payload.get("columns", []),
    }
    query = build_query_from_definition(table_definition, fallback_filters=matched_filters)
    all_keywords = table_keywords + [keyword for keyword in filter_keywords if keyword not in table_keywords]

    return {
        "input": user_input,
        "mode": "table",
        "selected_name": table_name,
        "table": table_name,
        "confidence": table_confidence,
        "matched_keywords": all_keywords,
        "filters": matched_filters,
        "query": query,
    }


def print_banner() -> None:
    """Render CLI banner."""
    banner = r"""
 _  __  ____  _         ____                           _
| |/ / / __ \| |       / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __
| ' / | |  | | |      | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
| . \ | |__| | |___   | |_| |  __/ | | |  __/ | | (_| | || (_) | |
|_|\_\ \___\_\_____|   \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|
"""
    print(banner)
    print("Internal KQL Generator for Microsoft Defender XDR Advanced Hunting")
    print("-" * 72)


def parse_args(argv: List[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="KQL query generator")
    parser.add_argument("query", nargs="*", help="Natural language hunting request")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    """CLI entrypoint."""
    args = parse_args(argv)
    print_banner()

    user_input = " ".join(args.query).strip()
    if not user_input:
        user_input = input("Enter your hunting request: ").strip()

    if not user_input:
        print("Error: query input cannot be empty.")
        return 1

    config_dir = Path(__file__).parent / "config"
    try:
        configs = load_all_configs(config_dir)
        result = generate_kql(user_input, configs)
    except (ConfigLoadError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1
    except Exception as exc:  # Defensive catch for unexpected runtime failures.
        print(f"Unexpected error: {exc}")
        return 1

    print(f"Selected mode: {result['mode']}")
    print(f"Selected detection/table: {result['selected_name']}")
    print(f"Confidence: {result['confidence']}")
    print("Generated KQL:")
    print(result["query"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
