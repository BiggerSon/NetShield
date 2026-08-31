from scapy.all import sniff

from app.config import CONFIG
from app.detector import process_packet


def start_capture(interface=None):

    if interface is None:
        interface = CONFIG["capture"].get("interface")

    print()
    print("[+] Packet capture başlatılıyor...")

    if interface:
        print(f"[+] Interface: {interface}")
    else:
        print("[+] Interface: Scapy default")

    sniff(
        iface=interface,
        prn=process_packet,
        store=False,
        promisc=CONFIG["capture"]["promiscuous"]
    )