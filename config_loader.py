"""Configuration loading utilities for the KQL generator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class ConfigLoadError(Exception):
    """Raised when a configuration file cannot be loaded."""


def load_json_config(config_dir: Path, filename: str) -> Dict[str, Any]:
    """Load one JSON configuration file from the provided directory."""
    file_path = config_dir / filename
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise ConfigLoadError(f"Config file not found: {file_path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigLoadError(f"Invalid JSON in file: {file_path}") from exc
    except OSError as exc:
        raise ConfigLoadError(f"Could not read config file: {file_path}") from exc

    if not isinstance(data, dict):
        raise ConfigLoadError(f"Config file must contain a JSON object: {file_path}")
    return data


def load_all_configs(config_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Load all required configuration files."""
    required_files = {
        "tables": "tables.json",
        "filters": "filters.json",
        "templates": "templates.json",
        "detections": "detections.json",
    }
    loaded: Dict[str, Dict[str, Any]] = {}
    for key, filename in required_files.items():
        loaded[key] = load_json_config(config_dir, filename)
    return loaded
