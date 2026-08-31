# 🛡️ NetShield IDS

> **Real-time Network Intrusion Detection System built with Python, Scapy and FastAPI.**

NetShield IDS is an open-source defensive security tool designed to monitor authorized network traffic, identify suspicious patterns, calculate risk levels, and notify the operator when potentially malicious activity is detected.

The project is designed to provide a lightweight alternative for learning and experimenting with network intrusion detection concepts.

---

## ✨ Features

### 🔍 Network Monitoring
- Real-time packet capture with Scapy
- Network interface selection
- Live packet statistics
- Automatic gateway discovery

### 🚨 Detection Engine
NetShield currently monitors for:

- ARP mapping changes / possible ARP spoofing
- SYN traffic anomalies
- UDP traffic anomalies
- ICMP traffic anomalies
- TCP port scanning
- Host scanning
- Unusual traffic patterns

### 🧠 Risk Engine
- IP-based risk scoring
- Severity levels: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`
- Adaptive traffic baselines
- Alert cooldown to reduce repeated notifications
- Risk score decay over time

### 🔔 Alerting
- Real-time terminal alerts
- Optional Windows notification beep
- Optional Discord webhook alerts
- Structured security event logs

### 📊 Reporting
- JSON event logs
- CSV event logs
- HTML security reports

### 🌐 Web Dashboard
The built-in FastAPI dashboard provides:

- Packet count
- Alert count
- Monitored host count
- Uptime
- Recent security events
- IP risk scores

---

## 🖥️ Dashboard

When NetShield is running, the web dashboard is available on the local machine.

Default address:

```text
http://127.0.0.1:8080
```

The dashboard refreshes automatically and displays the latest events detected by the IDS.

---

## 📋 Requirements

- Python `3.10+`
- Windows, Linux, or macOS
- Scapy
- FastAPI
- Uvicorn
- PyYAML
- Requests

### Windows

Windows users need **Npcap** installed for packet capture.

When installing Npcap, the default installation options are generally suitable for normal packet-capture use.

### Permissions

Packet capture may require elevated privileges depending on the operating system and network interface.

On Windows, if packet capture does not work, try running PowerShell or Command Prompt as **Administrator**.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/BiggerSon/NetShield.git
cd NetShield
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running NetShield

Start the IDS:

```bash
python main.py
```

NetShield will display the available network interfaces.

Example:

```text
========================================================================
                 🛡️ NETSHIELD IDS
                 Network Security Monitor
========================================================================
Version : 2.0.0

[+] Gateway detected: 192.168.1.1

[+] Detection modules:
    ARP Spoofing              : True
    SYN anomaly              : True
    UDP anomaly              : True
    ICMP anomaly             : True
    TCP port scan             : True
    Host scan                 : True
    Adaptive baseline         : True
    Automatic mitigation      : False

[+] Dashboard: http://127.0.0.1:8080

[+] NetShield çalışıyor.
[+] CTRL+C ile durdurabilirsin.
```

Select the network interface you want NetShield to monitor.

---

# 🎯 Selecting an Interface

You can let NetShield display the available interfaces:

```bash
python main.py
```

Or specify an interface directly:

```bash
python main.py --interface "YOUR_INTERFACE"
```

Replace `YOUR_INTERFACE` with the interface name shown by Scapy on your system.

If you are unsure which interface to use, start NetShield without the `--interface` argument and select the correct adapter from the list.

---

# ⚙️ Configuration

All main settings are stored in:

```text
config.yaml
```

You can enable or disable individual detection modules and change their thresholds.

Example:

```yaml
detection:
  window_seconds: 10

  syn:
    enabled: true
    threshold: 100

  udp:
    enabled: true
    threshold: 250

  icmp:
    enabled: true
    threshold: 100

  port_scan:
    enabled: true
    unique_ports: 20

  host_scan:
    enabled: true
    unique_hosts: 25

  arp:
    enabled: true
```

---

# 🧠 Adaptive Detection

NetShield can use an adaptive traffic baseline instead of relying only on fixed thresholds.

Configuration:

```yaml
adaptive:
  enabled: true
  multiplier: 3.0
  minimum_baseline: 10
```

This allows the detector to take previously observed traffic behavior into account.

Adaptive detection is intended to reduce false positives compared with using fixed thresholds alone.

---

# 🚨 Alert System

Terminal alerts are enabled by default:

```yaml
alerts:
  console: true
```

Example:

```text
========================================================================
🚨 NETSHIELD SECURITY ALERT
========================================================================
Time       : 2026-08-31T17:02:31
Type       : TCP Port Scan
Severity   : HIGH
Risk       : 81/100
Source     : 192.168.1.25
Destination: 192.168.1.1
Message    : Multiple destination ports observed from one source.
========================================================================
```

NetShield also uses an alert cooldown to prevent the same detection from flooding the console or notification service.

---

# 🔔 Discord Notifications

Discord notifications are optional.

In `config.yaml`:

```yaml
alerts:
  console: true

  discord:
    enabled: true
    webhook_url: "YOUR_WEBHOOK_URL"
```

Replace the placeholder with your own Discord webhook URL.

## ⚠️ Important

**Never commit a real webhook URL, API key, token, password, or other secret to GitHub.**

Keep sensitive values outside the public repository whenever possible.

---

# 📊 Logs and Reports

Security events are stored in:

```text
logs/security_events.json
logs/security_events.csv
```

The JSON format is useful for applications and automation.

The CSV format is useful for spreadsheets and data analysis.

---

# 📄 HTML Security Report

Generate an HTML report from the recorded events:

```bash
python main.py --report
```

The report will be created at:

```text
reports/security_report.html
```

---

# 🧪 Testing

The project includes basic tests for the risk engine.

Install pytest if it is not already installed:

```bash
pip install pytest
```

Run the tests:

```bash
pytest
```

---

# 📁 Project Structure

```text
NetShield/
│
├── main.py
├── config.yaml
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── state.py
│   ├── alerts.py
│   ├── risk.py
│   ├── detector.py
│   ├── capture.py
│   ├── reporter.py
│   └── discovery.py
│
├── web/
│   ├── __init__.py
│   ├── server.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── style.css
│       └── app.js
│
├── logs/
│   └── .gitkeep
│
├── reports/
│   └── .gitkeep
│
└── tests/
    └── test_risk.py
```

---

# 🛡️ Security Model

NetShield is an **IDS (Intrusion Detection System)**.

Its primary purpose is:

```text
Capture
   ↓
Analyze
   ↓
Detect
   ↓
Score
   ↓
Alert
   ↓
Log
   ↓
Report
```

Automatic mitigation is disabled by default:

```yaml
mitigation:
  enabled: false
```

This is intentional.

A detection system should not automatically block traffic based on a single potentially incorrect detection without a carefully designed response policy.

---

# ⚠️ False Positives

Network behavior can vary significantly depending on:

- Number of devices
- Network speed
- Applications
- Cloud services
- DNS activity
- Games
- Streaming
- Software updates
- Network topology

Therefore, a detection event does **not automatically mean that an attack is occurring**.

Thresholds should be adjusted according to the monitored environment.

---

# 🔐 Responsible Use

NetShield is intended for:

- Your own devices
- Your own networks
- Lab environments
- Authorized security testing
- Defensive network monitoring
- Cybersecurity education and research

**Only monitor network traffic that you are authorized to inspect.**

Do not use NetShield to monitor networks, devices, or traffic without appropriate authorization.

---

# 🤝 Contributing

Contributions are welcome.

Before opening a pull request:

1. Test your changes.
2. Do not include secrets or credentials.
3. Keep security-sensitive configuration out of commits.
4. Update the documentation when necessary.
5. Keep changes focused and explain the purpose of the change.

Ideas for future development include:

- More protocol detectors
- Better baseline learning
- PCAP import and analysis
- Advanced event correlation
- Authentication for the dashboard
- Database-backed event storage
- Additional notification providers
- Improved visualization
- Optional defensive response mechanisms

---

# 📜 License

NetShield IDS is released under the MIT License.

See the `LICENSE` file for the complete license text.

---

# ⭐ Project Status

**Current version:** `2.0.0`

NetShield is an actively developing defensive network-monitoring project.

The current release focuses on real-time detection, alerting, risk scoring, logging, reporting, and a lightweight web dashboard.

---

## 🛡️ NetShield IDS

**Monitor. Detect. Alert.**

Built with:

- Python
- Scapy
- FastAPI
- Uvicorn
- PyYAML
- Requests
