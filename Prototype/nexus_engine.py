# =================================================================
# NEXUS SECURITY SENTINEL - ADVANCED AI ENGINE (v3.0)
# =================================================================
# Developer: MD Taufique | Target OS: RHEL 9
# Core Features: Automated Incident Response (AIR), Progressive Penalty, Auto-Heal

import time
import random
from datetime import datetime

class NexusSentinelPro:
    def __init__(self):
        self.is_monitoring = True
        self.threat_intel = ["SQL_INJECTION", "BRUTE_FORCE", "ZERO_DAY_ANOMALY", "DDOS_SYN"]
        
        # State Management
        self.offense_tracker = {}  # Tracks how many times an IP attacked {ip: count}
        self.active_blocks = {}    # Tracks IPs currently in Cooldown {ip: unblock_time}
        self.permanent_bans = []   # IPs that are permanently blacklisted
        
        self.cooldown_seconds = 10 # Short block for first-time offenders

        print("=" * 65)
        print("[+] NEXUS SENTINEL CORE INITIALIZATION")
        print("[+] Sovereign Defense Mode : ACTIVE")
        print("[+] Progressive Penalty  : ACTIVE (Soft Block -> Hard Ban)")
        print("[+] Auto-Heal Protocol   : ACTIVE")
        print("=" * 65 + "\n")

    def get_timestamp(self):
        return datetime.now().strftime("%H:%M:%S")

    def analyze_traffic(self):
        # Simulating DPI (Deep Packet Inspection) returning a risk score
        return random.random()

    def trigger_air_protocol(self, attacker_ip, threat_type):
        """
        Automated Incident Response with Progressive Penalty System.
        """
        # Increment offense count for this IP
        self.offense_tracker[attacker_ip] = self.offense_tracker.get(attacker_ip, 0) + 1
        offenses = self.offense_tracker[attacker_ip]

        print(f"\n[{self.get_timestamp()}] [!] CRITICAL ALERT: {threat_type} detected from {attacker_ip}")

        if offenses == 1:
            # TIER 1: First Offense -> Temporary Soft Block (Auto-Heal enabled)
            unblock_time = time.time() + self.cooldown_seconds
            self.active_blocks[attacker_ip] = unblock_time
            print(f"[{self.get_timestamp()}] [*] ACTION: TIER 1 PENALTY APPLIED.")
            print(f"[{self.get_timestamp()}] [SUCCESS] IP {attacker_ip} isolated for {self.cooldown_seconds}s (Cooldown).")
            # os.system(f"sudo firewall-cmd --add-rich-rule='...reject'")
        
        else:
            # TIER 2: Repeat Offender -> Permanent Hard Ban (No Auto-Heal)
            self.permanent_bans.append(attacker_ip)
            if attacker_ip in self.active_blocks:
                del self.active_blocks[attacker_ip]
            print(f"[{self.get_timestamp()}] [*] ACTION: TIER 2 PENALTY APPLIED (REPEAT OFFENDER).")
            print(f"[{self.get_timestamp()}] [BLACKLIST] IP {attacker_ip} PERMANENTLY QUARANTINED.")
            # os.system(f"sudo firewall-cmd --add-rich-rule='...drop'")

        print("-" * 65)

    def process_auto_heal(self):
        """
        Checks for IPs whose cooldown period has expired and restores their access.
        """
        current_time = time.time()
        healed_ips = []

        for ip, unblock_time in list(self.active_blocks.items()):
            if current_time >= unblock_time:
                healed_ips.append(ip)
                del self.active_blocks[ip]
        
        for ip in healed_ips:
            print(f"\n[{self.get_timestamp()}] [+] AUTO-HEAL: Cooldown expired for {ip}.")
            print(f"[{self.get_timestamp()}] [+] ACTION: Removing firewall restriction. Integrity Restored.")
            print("-" * 65)
            # os.system(f"sudo firewall-cmd --remove-rich-rule='...reject'")

    def run(self):
        print(f"[{self.get_timestamp()}] Sentinel is guarding the infrastructure. Press Ctrl+C to stop.\n")
        try:
            while self.is_monitoring:
                # 1. Always check if any IP needs to be Auto-Healed
                self.process_auto_heal()

                # 2. Scan network traffic
                risk_score = self.analyze_traffic()

                # 3. Simulate high risk (over 85%)
                if risk_score > 0.85:
                    # Simulating a limited pool of IPs so we can see repeat offenders
                    fake_ip = f"192.168.64.{random.choice([10, 11, 12, 13])}"
                    
                    # Only attack if the IP is not currently blocked or permanently banned
                    if fake_ip not in self.active_blocks and fake_ip not in self.permanent_bans:
                        attack_name = random.choice(self.threat_intel)
                        self.trigger_air_protocol(fake_ip, attack_name)
                else:
                    status = f"[{self.get_timestamp()}] [SCAN] Traffic Safe | Risk: {risk_score:.2f} | Temp Blocks: {len(self.active_blocks)} | Perm Bans: {len(self.permanent_bans)}    "
                    print(status, end="\r")

                time.sleep(1.5)

        except KeyboardInterrupt:
            print(f"\n\n[{self.get_timestamp()}] [SHUTDOWN] Sentinel Engine safely offline.")

if __name__ == "__main__":
    app = NexusSentinelPro()
    app.run()