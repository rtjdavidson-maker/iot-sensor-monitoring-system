# IoT Sensor Telemetry & Alert Monitoring System

A **Python systems integration portfolio project** that simulates telemetry from ESP32-style sensors, checks readings against configurable thresholds, stores results in an SQLite database, and generates an HTML dashboard.

> **Scope:** Educational simulation. No ESP32 hardware, real sensor, network connection, or physical-device measurement is involved yet. This software is not intended for safety-critical use.

## What it demonstrates

- Software-to-device interface concepts using **structured sensor readings**
- Python modules, data classes, repeatable simulations, and automated fault detection
- Configurable operating thresholds for temperature, humidity, and voltage
- **SQL/SQLite** storage and querying
- Generation of a browser-readable **HTML dashboard** without third-party packages
- Python unit tests and **GitHub Actions** continuous integration

## Requirements

Python 3.10 or newer; no `pip` installations required.

## Run on Windows

Extract the ZIP, open File Explorer to the folder containing `main.py`, click its address bar, type `cmd`, and press Enter. Then run:

```cmd
python main.py
start "" "output\dashboard.html"
```

Run the automated tests:

```cmd
python -m unittest discover -s tests -v
```

## System flow

```text
simulator.py  ->  monitor.py  ->  storage.py  ->  dashboard.py
 Generate          Evaluate       SQLite           HTML
  readings          alerts        database       visualization
```

`main.py` orchestrates the pipeline. The simulator generates **30 readings from 3 virtual devices** (10 samples each). It deliberately includes outliers to test alert handling.

## Default engineering thresholds

| Measurement | Accepted range |
|---|---|
| Temperature | 10–35 °C |
| Relative humidity | 20–80% |
| Simulated voltage | 3.0–3.4 V |

These are educational example thresholds, not manufacturer requirements.

## Project layout

```text
iot-sensor-monitoring-system/
├── main.py             # Run the system
├── simulator.py        # Generate deterministic sensor data
├── monitor.py          # Validate readings and emit alerts
├── storage.py          # Store and retrieve data in SQLite
├── dashboard.py        # Render HTML dashboard
├── tests/
│   └── test_project.py # 12 automated unit tests
├── .github/workflows/
│   └── tests.yml       # CI testing
├── .gitignore
└── README.md
```

The `output/` folder is automatically created by the program, then excluded from Git commits because the database and report are generated artifacts.

## Learning exercises

1. In `monitor.py`, change `max_temperature` from 35 to 32 and predict how the alert count changes.
2. In `simulator.py`, change `samples_per_device` from 10 to 20 by passing `samples_per_device=20` into `generate_readings()` in `main.py`.
3. Add a test for a humidity reading of 85%.
4. Explain why the database uses a composite primary key `(device_id, sample_number)`.

## Planned extensions

- Read **actual ESP32 serial telemetry** using a USB connection and an appropriately tested serial library
- Add timestamped readings and historical trends
- Expose a local REST API and interactive filtering
- Add dashboard screenshots to the repository

## Career relevance

Relevant to **Systems Integration, Test Automation, Embedded Systems, IoT Software, and Validation Engineering**. The project currently proves simulation, validation, storage, testing, and visualization—not physical-device integration.
