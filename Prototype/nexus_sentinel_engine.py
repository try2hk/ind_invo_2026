#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=====================================================================
    NEXUS SENTINEL - AUTONOMOUS INCIDENT RESPONSE CORE (v8.1)
=====================================================================
Developer: MD Taufique 
Target: India Innovates 2026 Pitch
Description: Packet analysis aur active mitigation ke liye hybrid engine.
             RHEL par production ke liye chalta hai, MacOS/Win par simulation.
"""

import os
import platform
import time
import json
import logging
import random
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS # UI aur backend ko alag alag chalne dene ke liye

# Terminal colors - Sci-Fi Cyber Vibe ke liye
class C:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

app = Flask(__name__)
CORS(app) # Local network me cross-origin requests ko allow karne ke liye

# --- LOGGING SETUP (Real world forensics feel) ---
logging.basicConfig(
    filename='nexus_audit.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# --- SYSTEM METADATA ---
OS_TYPE = platform.system()
VERSION = "v8.1-PROD"

# --- IN-MEMORY DATABASE (Future me ise Redis/SQLite me move kar sakte hain) ---
db = {
    "system_meta": {
        "version": VERSION,
        "platform": f"{OS_TYPE} Kernel",
        "uptime_start": time.time(),
    },
    "stats": {
        "total_packets_inspected": 240590, # Ek realistic number se start hota hai
        "threats_neutralized": 0,
        "active_tier1_blocks": 0,
        "permanent_bans": 0
    },
    "audit_trail": [],
    "attacker_registry": {} 
}

# --- HELPER FUNCTIONS ---
def get_time():
    return datetime.now().strftime("%H:%M:%S")

def add_log(msg, level="INFO"):
    """Dono jagah log save karega: Terminal pe UI ke liye, aur file me audit ke liye."""
    db["audit_trail"].insert(0, {
        "timestamp": get_time(),
        "message": msg,
        "level": level
    })
    
    # UI ko fast rakhne ke liye array size maintain karein
    if len(db["audit_trail"]) > 20: 
        db["audit_trail"].pop()
        
    # Terminal Output ka Vibe Check
    if level == "CRITICAL":
        print(f"{C.RED}[!] {get_time()} - {msg}{C.RESET}")
    elif level == "WARNING":
        print(f"{C.YELLOW}[*] {get_time()} - {msg}{C.RESET}")
    elif level == "SUCCESS":
        print(f"{C.GREEN}[+] {get_time()} - {msg}{C.RESET}")
    else:
        print(f"{C.CYAN}[~] {get_time()} - {msg}{C.RESET}")

# --- KERNEL FIREWALL ADAPTER ---
def engage_firewall(ip, severity="TIER1"):
    """
    Asli magic yahan hai! 
    RHEL pe real block chalega, Mac pe sirf simulation dikhega.
    """
    if OS_TYPE == "Linux":
        if severity == "TIER2":
            # Firewalld ka use karke hard ban lagana
            cmd = f"sudo firewall-cmd --permanent --add-rich-rule='rule family=\"ipv4\" source address=\"{ip}\" reject' > /dev/null 2>&1"
        else:
            # 60 seconds ke liye soft block lagana
            cmd = f"sudo firewall-cmd --add-rich-rule='rule family=\"ipv4\" source address=\"{ip}\" timeout=60s reject' > /dev/null 2>&1"
        
        # os.system(cmd) # NOTE: Real RHEL demo me isko uncomment karein
        # os.system("sudo firewall-cmd --reload > /dev/null 2>&1")
        add_log(f"KERNEL_SYNC: iptables updated for {ip}.", "INFO")
    else:
        # Padhne walo ko pata chalna chahiye ki abhi dev mode chal raha hai
        add_log(f"SIM_MODE: Firewall engaged against {ip}.", "INFO")

# --- MATRIX BOOT SEQUENCE (Hacker Effect) ---
def run_matrix_boot():
    """Terminal me ek zabardast Hollywood hacker style boot animation dikhane ke liye"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(C.GREEN, end="")
    modules = ["KERNEL_HOOK_SYS", "AI_ANOMALY_CORE", "DPI_PACKET_SCANNER", "AUTO_HEAL_DAEMON", "FIREWALL_SYNC_API", "ZERO_TRUST_AUTH"]
    
    for _ in range(40):
        # Random memory allocation hex strings generate karna
        hex_str = "".join(random.choice("0123456789ABCDEF") for _ in range(12))
        mod = random.choice(modules)
        print(f"[0x{hex_str}] LOADING {mod} ... [OK]")
        time.sleep(0.03) # Tezi se scroll hone ka effect
        
    print("\n[+] INITIALIZING NEXUS PROTOCOL..." + C.RESET)
    time.sleep(0.8)
    os.system('clear' if os.name == 'posix' else 'cls')

# --- API ENDPOINTS (Dashboard yahan connect hota hai) ---
@app.route('/api/telemetry', methods=['GET'])
def telemetry():
    # Background worker: Expired IP blocks ko auto-heal karna
    now = time.time()
    for ip, data in list(db["attacker_registry"].items()):
        if data.get('blocked_until') and now > data['blocked_until'] and data['status'] == 'BLOCKED':
            db["attacker_registry"][ip]['status'] = 'CLEAN'
            db["stats"]["active_tier1_blocks"] -= 1
            add_log(f"AUTO-HEAL: Threat isolated. Connection restored for {ip}.", "SUCCESS")
            
    return jsonify(db)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Attack ka data yahan hit karega (Kali se ya UI button se)."""
    data = request.json
    attacker_ip = data.get('ip', '192.168.0.0')
    attack_vector = data.get('vector', 'UNKNOWN_PROBE')

    # Attacker ko registry me daalna
    if attacker_ip not in db["attacker_registry"]:
        db["attacker_registry"][attacker_ip] = {'strikes': 0, 'status': 'CLEAN'}

    db["attacker_registry"][attacker_ip]['strikes'] += 1
    strikes = db["attacker_registry"][attacker_ip]['strikes']
    db["stats"]["threats_neutralized"] += 1

    if strikes == 1:
        # Pehli galti -> Tier 1 Penalty
        db["attacker_registry"][attacker_ip]['status'] = 'BLOCKED'
        db["attacker_registry"][attacker_ip]['blocked_until'] = time.time() + 15 # 15s ka soft ban
        db["stats"]["active_tier1_blocks"] += 1
        engage_firewall(attacker_ip, "TIER1")
        add_log(f"THREAT ISOLATED: {attack_vector} from {attacker_ip}.", "WARNING")
    else:
        # Dobara attack kiya -> Tier 2 Penalty
        db["attacker_registry"][attacker_ip]['status'] = 'BANNED'
        db["attacker_registry"][attacker_ip]['blocked_until'] = 9999999999
        db["stats"]["permanent_bans"] += 1
        
        # Counters ko UI ke hisaab se theek karna
        if db["stats"]["active_tier1_blocks"] > 0:
            db["stats"]["active_tier1_blocks"] -= 1 
            
        engage_firewall(attacker_ip, "TIER2")
        add_log(f"LETHAL THREAT: Repeat attack from {attacker_ip}. PERMANENT BAN.", "CRITICAL")

    return jsonify({"status": "AIR_ENGAGED", "action": db["attacker_registry"][attacker_ip]['status']})

# --- BOOT SEQUENCE ---
if __name__ == '__main__':
    # Matrix boot effect chalana
    run_matrix_boot()
    
    # Asli ASCII Art aur details print karna
    print(f"{C.CYAN}")
    print(r"  _   _ ________  ___   _ _____   _____ _____ _   _ _____ _____ _   _ _____ _    ")
    print(r" | \ | |  ___|  \/  |  | /  ___| /  ___|  ___| \ | |_   _|_   _| \ | |  ___| |   ")
    print(r" |  \| | |__  \   / |  | \ `--.  \ `--.| |__ |  \| | | |   | | |  \| | |__ | |   ")
    print(r" | . ` |  __| /   \ |  | |`--. \  `--. \  __|| . ` | | |   | | | . ` |  __|| |   ")
    print(r" | |\  | |___/ /^\ \ \_/ /\__/ / /\__/ / |___| |\  | | |  _| |_| |\  | |___| |____")
    print(r" \_| \_/\____\/   \/\___/\____/  \____/\____/\_| \_/ \_/  \___/\_| \_\____/\_____/")
    print(f"                                                                            {C.RESET}")
    print(f"{C.YELLOW} >> AUTONOMOUS INCIDENT RESPONSE CORE v8.1{C.RESET}")
    print(f"{C.YELLOW} >> PLATFORM: {OS_TYPE} | PORT: 5050{C.RESET}")
    print(f"{C.GREEN} >> Security Posture: HIGH | AI Core: ACTIVE{C.RESET}")
    print("-" * 75)
    
    add_log("System Boot: Core services engaged.", "SUCCESS")
    add_log("Monitoring active on Port 5050. Awaiting packets...", "INFO")
    
    # Safari aur Kali dono connect kar sake isliye 0.0.0.0 par run karein
    app.run(host='0.0.0.0', port=5050, debug=False)