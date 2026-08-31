from collections import defaultdict, deque
from threading import Lock
import time


class NetworkState:

    def __init__(self):
        self.lock = Lock()
        self.syn = defaultdict(deque)
        self.udp = defaultdict(deque)
        self.icmp = defaultdict(deque)
        self.ports = defaultdict(set)
        self.hosts = defaultdict(set)
        self.arp_table = {}
        self.baseline = defaultdict(float)
        self.risk_scores = defaultdict(int)
        self.events = deque(maxlen=500)
        self.alert_history = {}
        self.total_packets = 0
        self.total_alerts = 0
        self.started_at = time.time()

    def add_packet(self):
        with self.lock:
            self.total_packets += 1

    def add_event(self, event):
        with self.lock:
            self.events.appendleft(event)
            self.total_alerts += 1

    def get_events(self):
        with self.lock:
            return list(self.events)

    def get_stats(self):
        with self.lock:
            return {
                "packets": self.total_packets,
                "alerts": self.total_alerts,
                "hosts": len(self.risk_scores),
                "uptime": int(time.time() - self.started_at)
            }


STATE = NetworkState()