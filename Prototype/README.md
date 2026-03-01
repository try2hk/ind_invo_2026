🛡️ Nexus Security Sentinel

Autonomous Incident Response (AIR) for Sovereign Infrastructure

Hey everyone! I'm MD Taufique, Lead Developer of Team Nexus Security, and this is our official submission for India Innovates 2026.

Welcome to the Nexus Sentinel repository. This isn't just a coding project for me; it's an attempt to solve a massive real-world problem I've noticed with our national digital infrastructure.

⚠️ Why I Built This

Most government servers (like MCD databases and local municipal nodes) run on legacy systems. When a cyber attack happens, it takes hours for a human admin to analyze the logs, figure out the attacker's IP, and manually block it. In that time, the data is already gone.

I wanted to build a system that doesn't wait for a human. It detects, it reacts, and it heals. Automatically in milliseconds.

🚀 The Core Vision (How it works)

Nexus Sentinel sits on top of RHEL 9 (Red Hat Enterprise Linux) and acts as an AI-driven shield. I've designed it with a Progressive Defense System:

Tier 1 Penalty (The Soft Block): If an IP acts suspiciously, the system blocks it temporarily (e.g., 10 seconds).

Auto-Heal Protocol: After the cooldown, the system automatically removes the block. This ensures legitimate users (false positives) aren't locked out of government services forever.

Tier 2 Penalty (The Hard Ban): If the same IP attacks again after healing, the system realizes it's a persistent threat/bot and drops a permanent kernel-level ban.

📂 Repository Structure

I've split the project into two parts to keep things organized:

📁 /prototype/ <- (WE ARE HERE)

This is my Proof of Concept (POC) for the selection phase.

nexus_engine.py: The Python backend that simulates packet scanning and progressive penalty logic.

dashboard.html: The advanced SOC Dashboard (with Gemini AI) to see the live simulation.

📁 /main/ <- (WORK IN PROGRESS)

This is where the actual production code will live.

I'm currently working on bridging the Python engine directly with firewall-cmd and building a Flask API.

🛠️ How to run the Prototype?

If you want to see the system in action:

Clone this repo and navigate to the /prototype/ folder.

Run the engine: python3 nexus_engine.py

Open dashboard.html in Chrome/Safari to see the visual representation of the engine blocking and healing in real-time.

📝 Developer's Note (TODOs)

[x] Build the core progressive penalty logic.

[x] Design the Dark Mode SOC Dashboard.

[x] Integrate Gemini API for instant threat analysis reporting.

[ ] Connect nexus_engine.py with actual RHEL OS kernel commands.

[ ] Package the whole thing into a single install.sh script for easy deployment.

Built with passion, late-night coding sessions, and countless cups of tea by MD Taufique (Nexus Security).