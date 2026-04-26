# KQL Generator

Internal rule-based KQL query generator for Microsoft Defender XDR Advanced Hunting.

## Features

- Loads all table, filter, detection, and template definitions from JSON configs in `config/`.
- Scores detections first using keyword matching from natural language input.
- Falls back to table + filter mode if no detection matches.
- Builds KQL with:
  - table
  - default time range (`1d`)
  - filters
  - optional summarize/post-filters
  - projected columns
  - `order by Timestamp desc`
  - `limit 50`
- Includes an interactive CLI with a banner.
- Uses only Python standard library for application runtime.

## Project Structure

```text
kql_generator/
├── main.py
├── config_loader.py
├── engine/
│   ├── __init__.py
│   ├── scorer.py
│   ├── filter_engine.py
│   ├── query_builder.py
│   └── selector.py
├── config/
│   ├── tables.json
│   ├── filters.json
│   ├── templates.json
│   └── detections.json
├── tests/
│   ├── test_scorer.py
│   ├── test_selector.py
│   └── test_query_builder.py
├── requirements.txt
└── README.md
```

## Usage

Run with inline query:

```bash
python main.py "find suspicious powershell"
```

Or interactive prompt mode:

```bash
python main.py
```

Then enter input like:

- `find suspicious powershell`
- `show failed login burst`
- `detect lolbins`
- `check phishing emails`
- `show url clicks`
- `detect registry persistence`

## Example Output

```text
Selected mode: detection
Selected detection/table: suspicious_powershell
Confidence: 0.5
Generated KQL:
DeviceProcessEvents
| where Timestamp >= ago(1d)
| where tolower(FileName) has "powershell"
| where tolower(ProcessCommandLine) has_any ("-enc", "-encodedcommand", "bypass")
| summarize Count=count() by DeviceName, AccountName, ProcessCommandLine
| where Count >= 1
| project DeviceName, AccountName, ProcessCommandLine, Count, Timestamp
| order by Timestamp desc
| limit 50
```

## Testing

Run tests with:

```bash
python -m unittest discover -s tests -v
```

## Error Handling

- Missing/invalid config files raise friendly errors.
- Empty input is rejected.
- If no detection or table can be matched, a clear error is returned.
