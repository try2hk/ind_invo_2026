🛡️ NEXUS SENTINEL - AUTONOMOUS DEFENSE GRID

India Innovates 2026 Hackathon Submission Developed by Team Nexus Security | Lead Innoveter : Md Taufique

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

nexus_sentinel_dash.html: The Glassmorphism-based SOC (Security Operations Center) Command Interface.

💻 Environment Setup & Testing Guide

This Proof of Concept (PoC) was successfully tested on a Red Hat Enterprise Linux (RHEL) environment.

1.Starting the Core Engine (On Target RHEL Server)
Navigate to the Proof_of_Concept directory and run the engine:

cd Proof_of_Concept 
pip3 install flask flask-cors 
python3 nexus_sentinel_engine.py

The engine will start monitoring on Port 9090.

2.Accessing the SOC Command Center
Open any web browser and navigate to the RHEL server's IP address:

http://<SERVER_IP_ADDRESS>:9090 
Example: http://http://192.168.64.3:9090

3.Simulating an Attack (From a Kali Linux Attacker Node)
To verify the autonomous mitigation, use a separate machine (like Kali Linux) to fire a simulated Zero-Day or Brute Force payload at the RHEL server.

Run the following curl command from the attacker machine (Replace 192.168.64.3 with your actual RHEL IP):

curl -X POST http://http://192.168.64.3:9090/api/analyze
-H "Content-Type: application/json"
-d '{"ip": "10.41.99.1", "vector": "SSH_BRUTE_FORCE"}'

4.Expected Output
First Strike: The engine detects the anomaly and triggers a Tier 1 Soft Block. The firewalld applies a 60-second timeout to the attacker IP.

Second Strike: If the command is run again, the engine registers a repeat offense and issues a Tier 2 Permanent Ban, modifying the firewall to permanently reject packets from the rogue node.

🔬 Phase 1 Roadmap: eBPF Kernel Hooks

We are actively researching the migration from user-space Python filtering to kernel-space eBPF (Extended Berkeley Packet Filter). This will allow the system to drop malicious packets at wire-speed (10Gbps+) with zero latency. See the Phase1_eBPF_Research/ folder for our initial C-based kernel hooks.

“Securing Code. Securing Governance. Securing the Nation.”