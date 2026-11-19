"""Check simulated IoT telemetry against configurable thresholds."""
from dataclasses import dataclass
from simulator import SensorReading


@dataclass(frozen=True)
class Limits:
    min_temperature: float = 10.0
    max_temperature: float = 35.0
    min_humidity: float = 20.0
    max_humidity: float = 80.0
    min_voltage: float = 3.0
    max_voltage: float = 3.4


def evaluate(reading: SensorReading, limits: Limits = Limits()) -> tuple[str, list[str]]:
    """Return an alert status and all failures for one reading."""
    reasons = []
    if not limits.min_temperature <= reading.temperature_c <= limits.max_temperature:
        reasons.append("Temperature outside allowed range")
    if not limits.min_humidity <= reading.humidity_pct <= limits.max_humidity:
        reasons.append("Humidity outside allowed range")
    if not limits.min_voltage <= reading.voltage_v <= limits.max_voltage:
        reasons.append("Voltage outside allowed range")
    return ("ALERT", reasons) if reasons else ("OK", [])
