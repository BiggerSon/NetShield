import time
import requests

from app.config import CONFIG
from app.models import SecurityEvent
from app.risk import calculate_score
from app.state import STATE
from app.reporter import save_event


def should_alert(event_type, source):

    key = f"{event_type}:{source}"

    current = time.time()

    cooldown = CONFIG["alerts"]["cooldown_seconds"]

    with STATE.lock:

        previous = STATE.alert_history.get(key)

        if previous is not None:
            if current - previous < cooldown:
                return False

        STATE.alert_history[key] = current

    return True


def send_discord(event: SecurityEvent):

    discord = CONFIG["alerts"]["discord"]

    if not discord.get("enabled"):
        return

    webhook = discord.get("webhook_url")

    if not webhook:
        return

    emoji = {
        "LOW": "🟢",
        "MEDIUM": "🟡",
        "HIGH": "🟠",
        "CRITICAL": "🔴"
    }.get(event.severity, "⚠️")

    payload = {
        "username": "NetShield IDS",
        "content": (
            f"{emoji} **NetShield Security Alert**\n\n"
            f"**Type:** {event.event_type}\n"
            f"**Severity:** {event.severity}\n"
            f"**Risk:** {event.risk_score}/100\n"
            f"**Source:** `{event.source}`\n"
            f"**Destination:** `{event.destination}`\n"
            f"**Message:** {event.message}"
        )
    }

    try:
        requests.post(
            webhook,
            json=payload,
            timeout=5
        )
    except Exception as exc:
        print(f"[!] Discord alert failed: {exc}")


def raise_alert(
    event_type,
    severity,
    source=None,
    destination=None,
    message="",
    details=None,
    score=None
):

    if not should_alert(event_type, source):
        return

    if score is None and source:
        score = calculate_score(
            event_type,
            severity,
            source
        )

    score = score or 0

    event = SecurityEvent(
        timestamp=__import__("datetime").datetime.now().isoformat(
            timespec="seconds"
        ),
        event_type=event_type,
        severity=severity,
        risk_score=score,
        source=source,
        destination=destination,
        message=message,
        details=details or {}
    )

    STATE.add_event(event)

    if CONFIG["alerts"]["console"]:

        print()
        print("=" * 72)
        print("🚨 NETSHIELD SECURITY ALERT")
        print("=" * 72)

        print(f"Time       : {event.timestamp}")
        print(f"Type       : {event.event_type}")
        print(f"Severity   : {event.severity}")
        print(f"Risk       : {event.risk_score}/100")
        print(f"Source     : {event.source}")
        print(f"Destination: {event.destination}")
        print(f"Message    : {event.message}")

        if event.details:
            print("Details    :")

            for key, value in event.details.items():
                print(f"  {key}: {value}")

        print("=" * 72)

    save_event(event)
    send_discord(event)