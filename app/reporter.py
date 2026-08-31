import csv
import json
import os

from app.config import CONFIG


def ensure_directories():

    json_file = CONFIG["logging"]["json_file"]
    csv_file = CONFIG["logging"]["csv_file"]

    os.makedirs(
        os.path.dirname(json_file),
        exist_ok=True
    )

    os.makedirs(
        os.path.dirname(csv_file),
        exist_ok=True
    )


def save_event(event):

    ensure_directories()

    data = event.to_dict()

    json_file = CONFIG["logging"]["json_file"]
    csv_file = CONFIG["logging"]["csv_file"]
    try:
        if os.path.exists(json_file):
            with open(
                json_file,
                "r",
                encoding="utf-8"
            ) as f:
                try:
                    records = json.load(f)

                    if not isinstance(records, list):
                        records = []

                except json.JSONDecodeError:
                    records = []

        else:
            records = []

        records.append(data)

        with open(
            json_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                records,
                f,
                indent=4,
                ensure_ascii=False
            )

    except Exception as exc:

        print(f"[!] JSON logging error: {exc}")
    try:

        file_exists = os.path.exists(csv_file)

        with open(
            csv_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            if not file_exists:

                writer.writerow([
                    "timestamp",
                    "event_type",
                    "severity",
                    "risk_score",
                    "source",
                    "destination",
                    "message",
                    "details"
                ])

            writer.writerow([
                data["timestamp"],
                data["event_type"],
                data["severity"],
                data["risk_score"],
                data["source"],
                data["destination"],
                data["message"],
                json.dumps(
                    data["details"],
                    ensure_ascii=False
                )
            ])

    except Exception as exc:

        print(f"[!] CSV logging error: {exc}")


def export_html():

    ensure_directories()

    json_file = CONFIG["logging"]["json_file"]

    if not os.path.exists(json_file):
        return None

    with open(
        json_file,
        "r",
        encoding="utf-8"
    ) as f:

        events = json.load(f)

    rows = []

    for event in reversed(events):

        rows.append(
            f"""
            <tr>
                <td>{event.get("timestamp", "")}</td>
                <td>{event.get("event_type", "")}</td>
                <td>{event.get("severity", "")}</td>
                <td>{event.get("risk_score", "")}</td>
                <td>{event.get("source", "")}</td>
                <td>{event.get("destination", "")}</td>
                <td>{event.get("message", "")}</td>
            </tr>
            """
        )

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NetShield Security Report</title>

<style>
body {{
    font-family: Arial, sans-serif;
    margin: 40px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px;
}}

th {{
    background: #222;
    color: white;
}}
</style>
</head>

<body>

<h1>NetShield IDS Security Report</h1>

<p>Total events: {len(events)}</p>

<table>

<tr>
<th>Time</th>
<th>Type</th>
<th>Severity</th>
<th>Risk</th>
<th>Source</th>
<th>Destination</th>
<th>Message</th>
</tr>

{"".join(rows)}

</table>

</body>
</html>
"""

    output = "reports/security_report.html"

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    return output