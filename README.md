# EMR Test Plugin

A simple Electronic Medical Record (EMR) demo plugin for testing and demonstration purposes.

## Features

- Display a mock EMR interface
- Enter patient demographics
- Record vital signs
- Enter clinical assessments and treatment plans
- Simulated save functionality

## Installation

```bash
pip install -e .
```

## Usage

The plugin provides a command `open_emr_record` that can be used to demonstrate EMR functionality:

```python
record_data = {
    "name": "John Smith",
    "dob": "1980-05-15",
    "mrn": "MRN123456",
    "vitals": {
        "bp": "118/78",
        "pulse": "90",
        "temp": "100.2",
        "weight": "175"
    },
    "assessment": "Patient presents with...",
    "plan": "1. Rest\n2. Hydration..."
}

# Open EMR record with data
open_emr_record(record_data)
```

## Requirements

- Python 3.7+
- Selenium 4.0.0+
- Chrome WebDriver

## License

MIT
