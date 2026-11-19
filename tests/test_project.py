import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from dashboard import generate_dashboard
from monitor import Limits, evaluate
from simulator import SensorReading, generate_readings
from storage import read_records, save_readings


class IoTProjectTests(unittest.TestCase):
    def test_simulation_deterministic(self):
        self.assertEqual(generate_readings(seed=4), generate_readings(seed=4))

    def test_simulation_count(self):
        self.assertEqual(len(generate_readings(2, 5)), 10)

    def test_invalid_counts(self):
        with self.assertRaises(ValueError):
            generate_readings(device_count=0)

    def test_good_reading(self):
        status, reasons = evaluate(SensorReading("A", 1, 22, 50, 3.3))
        self.assertEqual(status, "OK")
        self.assertEqual(reasons, [])

    def test_temperature_alert(self):
        status, reasons = evaluate(SensorReading("A", 1, 45, 50, 3.3))
        self.assertEqual(status, "ALERT")
        self.assertTrue(any("Temperature" in reason for reason in reasons))

    def test_multiple_alerts(self):
        status, reasons = evaluate(SensorReading("A", 1, 45, 90, 2.9))
        self.assertEqual(status, "ALERT")
        self.assertEqual(len(reasons), 3)

    def test_configurable_thresholds(self):
        status, _ = evaluate(SensorReading("A", 1, 33, 50, 3.3), Limits(max_temperature=30))
        self.assertEqual(status, "ALERT")

    def test_sqlite_round_trip(self):
        with TemporaryDirectory() as temp_dir:
            db = Path(temp_dir) / "output" / "data.db"
            readings = [SensorReading("A", 1, 24, 51, 3.2)]
            self.assertEqual(save_readings(readings, db), 1)
            result = read_records(db)
            self.assertEqual(result[0][0], "A")
            self.assertEqual(result[0][5], "OK")

    def test_sqlite_rerun_replaces_records(self):
        with TemporaryDirectory() as temp_dir:
            db = Path(temp_dir) / "data.db"
            save_readings([SensorReading("A", 1, 24, 51, 3.2)], db)
            save_readings([SensorReading("B", 1, 42, 51, 3.2)], db)
            self.assertEqual(len(read_records(db)), 1)
            self.assertEqual(read_records(db)[0][0], "B")

    def test_html_output(self):
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "dashboard.html"
            generate_dashboard([("Device-1", 1, 24, 51, 3.2, "OK", "")], output)
            self.assertIn("IoT Sensor Telemetry Dashboard", output.read_text(encoding="utf-8"))

    def test_html_escaping(self):
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "dashboard.html"
            generate_dashboard([("<script>", 1, 24, 51, 3.2, "ALERT", "<bad>")], output)
            text = output.read_text(encoding="utf-8")
            self.assertIn("&lt;script&gt;", text)
            self.assertNotIn("<script>", text)

    def test_empty_dashboard_rejected(self):
        with TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError):
                generate_dashboard([], Path(temp_dir) / "report.html")


if __name__ == "__main__":
    unittest.main()
