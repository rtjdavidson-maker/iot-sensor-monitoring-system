"""Persist simulated IoT telemetry in an SQLite database."""
import sqlite3
from pathlib import Path
from simulator import SensorReading
from monitor import evaluate


def save_readings(readings: list[SensorReading], destination: Path) -> int:
    """Replace existing simulation data; returns inserted record count."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(destination) as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS telemetry (
            device_id TEXT NOT NULL,
            sample_number INTEGER NOT NULL,
            temperature_c REAL NOT NULL,
            humidity_pct REAL NOT NULL,
            voltage_v REAL NOT NULL,
            status TEXT NOT NULL,
            reason TEXT NOT NULL,
            PRIMARY KEY (device_id, sample_number)
        )""")
        connection.execute("DELETE FROM telemetry")
        records = []
        for reading in readings:
            status, reasons = evaluate(reading)
            records.append((reading.device_id, reading.sample_number, reading.temperature_c,
                            reading.humidity_pct, reading.voltage_v, status, "; ".join(reasons)))
        connection.executemany("""INSERT INTO telemetry VALUES (?, ?, ?, ?, ?, ?, ?)""", records)
        connection.commit()
    return len(records)


def read_records(database: Path) -> list[tuple]:
    with sqlite3.connect(database) as connection:
        return connection.execute("""SELECT device_id, sample_number, temperature_c,
            humidity_pct, voltage_v, status, reason FROM telemetry
            ORDER BY device_id, sample_number""").fetchall()
