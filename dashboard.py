"""Render stored telemetry into a local, browser-readable HTML dashboard."""
from collections import Counter
from html import escape
from pathlib import Path


def generate_dashboard(records: list[tuple], destination: Path) -> None:
    if not records:
        raise ValueError("No telemetry records supplied")
    total = len(records)
    counts = Counter(row[5] for row in records)
    alert_count = counts["ALERT"]
    rows = []
    for device, sample, temperature, humidity, voltage, status, reason in records:
        badge_class = "alert" if status == "ALERT" else "ok"
        rows.append(f"<tr><td>{escape(device)}</td><td>{sample}</td><td>{temperature:.1f}</td>"
                    f"<td>{humidity:.1f}</td><td>{voltage:.2f}</td>"
                    f'<td class="{badge_class}">{escape(status)}</td><td>{escape(reason) or "—"}</td></tr>')
    html = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IoT Telemetry Monitoring Dashboard</title>
<style>
:root{font-family:system-ui,sans-serif;color:#ecf3fb;background:#0b1220}
body{max-width:1150px;margin:35px auto;padding:0 20px}
h1{font-size:clamp(1.5rem,4vw,2.5rem)}p{color:#afc1d4}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:24px 0}
.card,.panel{background:#19283b;border:1px solid #314760;border-radius:12px;padding:18px}
.card b{display:block;font-size:2rem;margin-top:8px}
.panel{overflow-x:auto}
table{width:100%;border-collapse:collapse;min-width:800px}
th,td{text-align:left;padding:10px;border-bottom:1px solid #35485e;font-size:.9rem}
.ok{color:#55e4b6;font-weight:700}.alert{color:#ff8d9c;font-weight:700}
</style></head><body><h1>IoT Sensor Telemetry Dashboard</h1>
<p>Educational simulator · No real sensors or network connections</p>
<section class="cards"><div class="card">Samples<b>""" + str(total) + """</b></div>
<div class="card">Devices<b>""" + str(len({row[0] for row in records})) + """</b></div>
<div class="card">Alerts<b>""" + str(alert_count) + """</b></div>
<div class="card">Alert rate<b>""" + f"{alert_count / total:.1%}" + """</b></div></section>
<section class="panel"><h2>Device Telemetry &amp; Alerts</h2><table>
<thead><tr><th>Device</th><th>Sample</th><th>Temp (°C)</th><th>Humidity (%)</th><th>Voltage (V)</th><th>Status</th><th>Reason</th></tr></thead>
<tbody>""" + "".join(rows) + """</tbody></table></section>
<p>Thresholds: temperature 10–35 °C, humidity 20–80%, voltage 3.0–3.4 V.</p>
</body></html>"""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding="utf-8")
