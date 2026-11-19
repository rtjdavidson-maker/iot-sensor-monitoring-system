"""Run a complete simulated IoT collection -> validation -> storage -> dashboard pipeline."""
from pathlib import Path
from dashboard import generate_dashboard
from monitor import evaluate
from simulator import generate_readings
from storage import save_readings, read_records


def main() -> None:
    readings = generate_readings()
    db_path = Path("output") / "telemetry.sqlite3"
    count = save_readings(readings, db_path)
    records = read_records(db_path)
    alerts = sum(evaluate(reading)[0] == "ALERT" for reading in readings)
    dashboard_path = Path("output") / "dashboard.html"
    generate_dashboard(records, dashboard_path)
    print(f"Simulated {count} sensor measurements across 3 devices.")
    print(f"Alerts detected: {alerts}")
    print(f"Database: {db_path.resolve()}")
    print(f"Dashboard: {dashboard_path.resolve()}")
    print('To open the dashboard on Windows: start "" "output\\dashboard.html"')


if __name__ == "__main__":
    main()
