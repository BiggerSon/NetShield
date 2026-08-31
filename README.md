# 🛡️ NetShield IDS

**NetShield IDS** is an open-source Network Intrusion Detection System (IDS) written in Python.

It monitors authorized network traffic in real time and detects suspicious network activity using configurable detection rules, traffic baselines, and risk scoring.

---

## 🚨 Detection Capabilities

NetShield can detect and report suspicious patterns including:

- ARP mapping changes
- SYN traffic anomalies
- UDP traffic anomalies
- ICMP traffic anomalies
- TCP port scanning
- Host scanning
- Traffic baseline anomalies

---

## ✨ Features

- 🔍 Real-time packet monitoring
- 📡 Scapy-based packet capture
- 🧠 Adaptive traffic baseline
- 🎯 IP-based risk scoring
- 🚨 Real-time security alerts
- 📋 Security event logging
- 📄 JSON reports
- 📊 CSV reports
- 🌐 HTML security reports
- 🔔 Discord webhook alerts
- 🖥️ FastAPI web dashboard
- ⏱️ Alert cooldown system
- ⚙️ Configurable detection thresholds
- 🛡️ Automatic mitigation disabled by default

---

## 🖥️ Dashboard

NetShield includes a lightweight FastAPI dashboard for monitoring detected security events.

The dashboard provides:

- Total captured packets
- Total security alerts
- Monitored hosts
- System uptime
- Recent security events
- IP-based risk scores
