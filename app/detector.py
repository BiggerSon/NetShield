import time
from collections import deque

from scapy.all import IP, TCP, UDP, ICMP, ARP

from app.config import CONFIG
from app.state import STATE
from app.alerts import raise_alert


def clean_queue(queue, window):

    current = time.time()

    while queue and current - queue[0] > window:
        queue.popleft()


def adaptive_threshold(source, packet_type, configured):

    if not CONFIG["adaptive"]["enabled"]:
        return configured

    with STATE.lock:

        baseline = STATE.baseline[
            f"{source}:{packet_type}"
        ]

    minimum = CONFIG["adaptive"]["minimum_baseline"]

    if baseline < minimum:
        return configured

    adaptive = int(
        baseline *
        CONFIG["adaptive"]["multiplier"]
    )

    return max(
        configured,
        adaptive
    )


def update_baseline(source, packet_type, rate):

    key = f"{source}:{packet_type}"

    with STATE.lock:

        old = STATE.baseline.get(key, 0)

        if old == 0:
            STATE.baseline[key] = float(rate)

        else:
            # Exponential moving average
            STATE.baseline[key] = (
                old * 0.8 +
                rate * 0.2
            )


def detect_syn(packet):

    if not CONFIG["detection"]["syn"]["enabled"]:
        return

    if not packet.haslayer(IP):
        return

    if not packet.haslayer(TCP):
        return

    tcp = packet[TCP]

    # SYN without ACK
    if not (tcp.flags & 0x02):
        return

    if tcp.flags & 0x10:
        return

    src = packet[IP].src
    dst = packet[IP].dst

    with STATE.lock:

        queue = STATE.syn[src]

        queue.append(time.time())

        clean_queue(
            queue,
            CONFIG["detection"]["window_seconds"]
        )

        count = len(queue)

    threshold = adaptive_threshold(
        src,
        "syn",
        CONFIG["detection"]["syn"]["threshold"]
    )

    rate = count / CONFIG["detection"]["window_seconds"]

    update_baseline(src, "syn", rate)

    if count >= threshold:

        severity = "CRITICAL" if count >= threshold * 2 else "HIGH"

        score = min(
            100,
            int(
                60 +
                (count / threshold) * 20
            )
        )

        raise_alert(
            event_type="SYN Flood / SYN Anomaly",
            severity=severity,
            source=src,
            destination=dst,
            score=score,
            message="Unusually high SYN traffic detected.",
            details={
                "packets": count,
                "threshold": threshold,
                "window_seconds":
                    CONFIG["detection"]["window_seconds"]
            }
        )


def detect_udp(packet):

    if not CONFIG["detection"]["udp"]["enabled"]:
        return

    if not packet.haslayer(IP):
        return

    if not packet.haslayer(UDP):
        return

    src = packet[IP].src
    dst = packet[IP].dst

    with STATE.lock:

        queue = STATE.udp[src]

        queue.append(time.time())

        clean_queue(
            queue,
            CONFIG["detection"]["window_seconds"]
        )

        count = len(queue)

    threshold = adaptive_threshold(
        src,
        "udp",
        CONFIG["detection"]["udp"]["threshold"]
    )

    rate = count / CONFIG["detection"]["window_seconds"]

    update_baseline(src, "udp", rate)

    if count >= threshold:

        severity = "CRITICAL" if count >= threshold * 2 else "HIGH"

        raise_alert(
            event_type="UDP Flood / UDP Anomaly",
            severity=severity,
            source=src,
            destination=dst,
            score=min(100, 65 + int(count / threshold * 20)),
            message="Unusually high UDP traffic detected.",
            details={
                "packets": count,
                "threshold": threshold
            }
        )


def detect_icmp(packet):

    if not CONFIG["detection"]["icmp"]["enabled"]:
        return

    if not packet.haslayer(IP):
        return

    if not packet.haslayer(ICMP):
        return

    src = packet[IP].src
    dst = packet[IP].dst

    with STATE.lock:

        queue = STATE.icmp[src]

        queue.append(time.time())

        clean_queue(
            queue,
            CONFIG["detection"]["window_seconds"]
        )

        count = len(queue)

    threshold = adaptive_threshold(
        src,
        "icmp",
        CONFIG["detection"]["icmp"]["threshold"]
    )

    rate = count / CONFIG["detection"]["window_seconds"]

    update_baseline(src, "icmp", rate)

    if count >= threshold:

        raise_alert(
            event_type="ICMP Flood / ICMP Anomaly",
            severity="HIGH",
            source=src,
            destination=dst,
            score=min(
                100,
                60 + int(count / threshold * 20)
            ),
            message="Unusually high ICMP traffic detected.",
            details={
                "packets": count,
                "threshold": threshold
            }
        )


def detect_port_scan(packet):

    if not CONFIG["detection"]["port_scan"]["enabled"]:
        return

    if not packet.haslayer(IP):
        return

    if not packet.haslayer(TCP):
        return

    tcp = packet[TCP]

    if not (tcp.flags & 0x02):
        return

    src = packet[IP].src
    dst = packet[IP].dst

    with STATE.lock:

        STATE.ports[src].add(
            (dst, int(tcp.dport))
        )

        count = len(
            STATE.ports[src]
        )

    threshold = CONFIG["detection"]["port_scan"]["unique_ports"]

    if count >= threshold:

        raise_alert(
            event_type="TCP Port Scan",
            severity="HIGH",
            source=src,
            destination=dst,
            score=min(
                100,
                55 + count
            ),
            message="Multiple destination ports observed from one source.",
            details={
                "unique_targets_ports": count,
                "threshold": threshold
            }
        )


def detect_host_scan(packet):

    if not CONFIG["detection"]["host_scan"]["enabled"]:
        return

    if not packet.haslayer(IP):
        return

    if not packet.haslayer(TCP):
        return

    tcp = packet[TCP]

    if not (tcp.flags & 0x02):
        return

    src = packet[IP].src
    dst = packet[IP].dst

    with STATE.lock:

        STATE.hosts[src].add(dst)

        count = len(
            STATE.hosts[src]
        )

    threshold = CONFIG["detection"]["host_scan"]["unique_hosts"]

    if count >= threshold:

        raise_alert(
            event_type="Host Scan / Network Reconnaissance",
            severity="HIGH",
            source=src,
            destination=dst,
            score=min(
                100,
                50 + count
            ),
            message="One source contacted an unusually large number of hosts.",
            details={
                "unique_hosts": count,
                "threshold": threshold
            }
        )


def detect_arp(packet):

    if not CONFIG["detection"]["arp"]["enabled"]:
        return

    if not packet.haslayer(ARP):
        return

    arp = packet[ARP]

    # ARP reply
    if arp.op != 2:
        return

    ip = arp.psrc
    mac = arp.hwsrc.lower()

    if not ip or not mac:
        return

    with STATE.lock:

        previous = STATE.arp_table.get(ip)

        if previous is None:

            STATE.arp_table[ip] = mac

            return

        if previous == mac:
            return

        STATE.arp_table[ip] = mac

    raise_alert(
        event_type="ARP Spoofing / ARP Mapping Change",
        severity="CRITICAL",
        source=mac,
        destination=ip,
        score=95,
        message="An IP address was observed with a different MAC address.",
        details={
            "previous_mac": previous,
            "new_mac": mac,
            "ip": ip
        }
    )


def process_packet(packet):

    STATE.add_packet()

    try:

        detect_arp(packet)
        detect_syn(packet)
        detect_udp(packet)
        detect_icmp(packet)
        detect_port_scan(packet)
        detect_host_scan(packet)

    except Exception as exc:

        print(
            f"[!] Detection error: {exc}"
        )


def reset_scan_state():

    while True:

        time.sleep(
            CONFIG["detection"]["window_seconds"]
        )

        with STATE.lock:

            STATE.ports.clear()
            STATE.hosts.clear()