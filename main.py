import argparse
import threading
import time

import uvicorn

from app.capture import start_capture
from app.config import CONFIG
from app.detector import reset_scan_state
from app.discovery import discover_gateway
from app.reporter import export_html
from app.risk import decay_risk_scores


def print_banner():

    print()
    print("=" * 72)
    print("                 🛡️ NETSHIELD IDS")
    print("                 Network Security Monitor")
    print("=" * 72)
    print(f"Version : {CONFIG['app']['version']}")
    print()


def start_dashboard():

    if not CONFIG["dashboard"]["enabled"]:
        return

    uvicorn.run(
        "web.server:app",
        host=CONFIG["dashboard"]["host"],
        port=CONFIG["dashboard"]["port"],
        log_level="warning"
    )


def risk_decay_loop():

    while True:

        time.sleep(60)

        decay_risk_scores()


def main():

    parser = argparse.ArgumentParser(
        description="NetShield Network Intrusion Detection System"
    )

    parser.add_argument(
        "--interface",
        help="Network interface"
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate HTML report and exit"
    )

    args = parser.parse_args()

    print_banner()

    if args.report:

        report = export_html()

        if report:
            print(f"[+] Report oluşturuldu: {report}")

        else:
            print("[!] Henüz security event bulunamadı.")

        return

    gateway = discover_gateway()

    if gateway:

        print(f"[+] Gateway detected: {gateway}")

    else:

        print("[!] Gateway otomatik bulunamadı.")

    print()
    print("[+] Detection modules:")

    print(
        "    ARP Spoofing              : "
        f"{CONFIG['detection']['arp']['enabled']}"
    )

    print(
        "    SYN anomaly              : "
        f"{CONFIG['detection']['syn']['enabled']}"
    )

    print(
        "    UDP anomaly              : "
        f"{CONFIG['detection']['udp']['enabled']}"
    )

    print(
        "    ICMP anomaly             : "
        f"{CONFIG['detection']['icmp']['enabled']}"
    )

    print(
        "    TCP port scan            : "
        f"{CONFIG['detection']['port_scan']['enabled']}"
    )

    print(
        "    Host scan                : "
        f"{CONFIG['detection']['host_scan']['enabled']}"
    )

    print(
        "    Adaptive baseline        : "
        f"{CONFIG['adaptive']['enabled']}"
    )

    print(
        "    Automatic mitigation     : "
        f"{CONFIG['mitigation']['enabled']}"
    )

    # Scan state cleaner
    threading.Thread(
        target=reset_scan_state,
        daemon=True
    ).start()

    # Risk decay
    threading.Thread(
        target=risk_decay_loop,
        daemon=True
    ).start()

    # Dashboard
    if CONFIG["dashboard"]["enabled"]:

        dashboard_thread = threading.Thread(
            target=start_dashboard,
            daemon=True
        )

        dashboard_thread.start()

        print()
        print(
            "[+] Dashboard: "
            f"http://{CONFIG['dashboard']['host']}:"
            f"{CONFIG['dashboard']['port']}"
        )

    print()
    print("[+] NetShield çalışıyor.")
    print("[+] CTRL+C ile durdurabilirsin.")
    print()

    try:

        start_capture(
            args.interface
        )

    except KeyboardInterrupt:

        print()
        print("[+] NetShield kapatılıyor...")

    except PermissionError:

        print()
        print(
            "[!] Paket yakalama yetkisi yok."
        )

        print(
            "[!] Windows'ta terminali "
            "Yönetici olarak çalıştır."
        )

    except Exception as exc:

        print()
        print(f"[!] Fatal error: {exc}")


if __name__ == "__main__":
    main()