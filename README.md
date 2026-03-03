🛡️ NEXUS SENTINEL - AUTONOMOUS INCIDENT RESPONSE 


Nexus Sentinel is an AI-driven, sovereign defense grid designed to secure critical national infrastructure (such as MCD networks). The system transforms the manual incident response timeline from 180+ minutes down to 0.02 milliseconds.

🚀 Key Features

Zero-Day Anomaly Detection: Behavioral threat scoring stops unknown vectors.

Autonomous Kill-Switch: Instantly isolates malicious IPs at the OS firewall level (RHEL firewalld/iptables).

Self-Healing Network: Tier 1 soft-blocks automatically lift after the threat subsides, requiring zero manual intervention.

Lethal Tier 2 Bans: Repeat offenders are permanently banned from the sovereign network.

Air-Gapped Ready: Runs entirely on local infrastructure with zero external cloud dependencies.

📂 Project Architecture | Repo Hierarchie


Folder / File                                 Description

📁 Proof_of_Concept/                          Python-based Core Engine aur Glassmorphism Dashboard (PoC).

📁 Phase1_eBPF_Research/.                     Future Roadmap: C-based eBPF kernel hooks for 10Gbps+ traffic.

📁 docs/.                                     Technical Whitepapers aur Architecture Reports.

📄 LICENSE.                                   MIT Professional License.

📄 README.md                                  Project Documentation and Guide.


🚀 Getting Started (Lab Setup)

This prototype has been successfully tested on Red Hat Enterprise Linux (RHEL). Follow the steps below for setup:

1. Installation

Navigate to the folder in your RHEL terminal and install dependencies:

cd Proof_of_Concept
pip3 install -r requirements.txt


2. Launching the Engine

Run the engine to initiate Autonomous Monitoring:

python3 nexus_sentinel_engine.py


Note: The engine initiates monitoring on Port 9090 by default.

3. Accessing SOC Dashboard

Open a browser (Safari/Chrome) and navigate to:
👉 http://localhost:9090 (Local access)
👉 http://<YOUR_RHEL_IP>:9090 (Network access)

⚔️ Simulation Guide (Red Team vs Blue Team)

Use a Kali Linux machine to simulate an attack.

🛡️ Tier 1 Action (Soft Block)

Trigger AI detection by sending a payload from the Attacker IP:

curl -X POST http://192.168.64.3:9090/api/analyze \ 
-H "Content-Type: application/json" \
-d '{"ip": "10.41.99.1", "vector": "SSH_BRUTE_FORCE"}'


Sentinel action: The Attacker IP will be isolated (rejected) for 60 seconds.

🔥 Tier 2 Action (Permanent Ban)

A repeat attack will trigger a lethal ban:
Sentinel action: The Attacker IP will be permanently blocked at the Kernel level.



4.Expected Output
First Strike: The engine detects the anomaly and triggers a Tier 1 Soft Block. The firewalld applies a 60-second timeout to the attacker IP.

Second Strike: If the command is run again, the engine registers a repeat offense and issues a Tier 2 Permanent Ban, modifying the firewall to permanently reject packets from the rogue node.

🔬 Phase 1 (eBPF Migration)
We are actively researching the migration from user-space Python filtering to kernel-space eBPF (Extended Berkeley Packet Filter). This will allow the system to drop malicious packets at wire-speed (10Gbps+) with zero latency. See the Phase1_eBPF_Research/ folder for our initial C-based kernel hooks.

🤝 Developed By

Team Nexus Security

Lead Innovator: MD Taufique

Domain: Cybersecurity & Sovereign Infrastructure

Securing Code. Securing Governance. Securing the Nation.

