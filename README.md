🛡️ NEXUS SENTINEL

Autonomous Incident Response Core Project for India Innovates 2026 | Lead Innovator: MD Taufique

📌 Executive Summary

Nexus Sentinel is a sovereign, AI-driven autonomous defense grid designed specifically for Municipal and National Infrastructure (e.g., MCD networks). It transforms the legacy incident response timeline from 180+ minutes down to 0.02 milliseconds by utilizing Deep Packet Inspection (DPI) and Kernel-level netfilter isolation.

🚀 Key Features

Zero-Day Anomaly Detection: Behavioral threat scoring stops unknown vectors.

Autonomous Kill-Switch: Instantly isolates malicious IPs at the OS firewall level (RHEL firewalld/iptables).

Self-Healing Network: Tier 1 soft-blocks automatically lift after the threat subsides, requiring zero manual intervention.

Lethal Tier 2 Bans: Repeat offenders are permanently banned from the sovereign network.

Air-Gapped Ready: Runs entirely on local infrastructure with zero external cloud dependencies.

⚙️ Architecture

nexus_sentinel_engine.py: The Python-based Hybrid Defense Core. Connects directly to the OS kernel.

dashboard.html: The Glassmorphism-based SOC (Security Operations Center) Command Interface.

🛠️ How to Run (Simulation / Demo Mode)

Start the Core Engine:

pip install flask flask-cors
python3 nexus_sentinel_engine.py


Launch the Command Center:
Open dashboard.html in Safari/Chrome.

Trigger an Attack (from Kali Linux or Demo API):

curl -X POST http://localhost:5050/api/analyze \
-H "Content-Type: application/json" \
-d '{"ip": "10.41.99.1", "vector": "SSH_BRUTE_FORCE"}'


“Securing Code. Securing Governance. Securing the Nation.”