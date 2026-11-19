"""Deterministic simulated sensor telemetry. No physical hardware required."""
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class SensorReading:
    device_id: str
    sample_number: int
    temperature_c: float
    humidity_pct: float
    voltage_v: float


def generate_readings(device_count: int = 3, samples_per_device: int = 10, seed: int = 27) -> list[SensorReading]:
    """Create repeatable simulated readings, including occasional outliers."""
    if device_count < 1 or samples_per_device < 1:
        raise ValueError("device_count and samples_per_device must be positive")
    rng = random.Random(seed)
    readings = []
    for d in range(1, device_count + 1):
        for sample in range(1, samples_per_device + 1):
            temp = round(rng.uniform(18, 34), 1)
            humidity = round(rng.uniform(32, 75), 1)
            voltage = round(rng.uniform(3.15, 3.35), 2)
            if sample % 7 == 0:
                temp = round(rng.uniform(36, 42), 1)
            if sample % 9 == 0:
                voltage = round(rng.uniform(2.7, 2.95), 2)
            readings.append(SensorReading(f"ESP32-{d:02d}", sample, temp, humidity, voltage))
    return readings
