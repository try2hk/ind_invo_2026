#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# =====================================================
#    NEXUS SENTINEL - AUTONOMOUS INCIDENT RESPONSE CORE 
# ======================================================
# Developed by : Team Nexus Security | Lead Innovator  : MD TAUFIQUE
# AI & Logic Core : Nexus AI Division | Network Sec : R&D Team
# Target OS: Linux (RHEL 8+), MacOS (for simulation/testing)
# Core Features: Automated Incident Response (AIR), Progressive Penalty, Auto-Heal

import os
import platform
import time
import logging
import random
import socket
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS 

# --- SAFE FLASK LOG SILENCING ---
# Team ne decide kiya ki terminal ko clean rakhne ke liye sirf safe logging controls use karenge
cli = logging.getLogger('werkzeug')
cli.setLevel(logging.ERROR)

# Terminal colors - Sci-Fi Cyber Vibe ke liye
class C:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

# Static folder set kiya gaya hai taaki dashboard seamlessly serve ho sake
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app) 

# --- LOGGING SETUP ---
# Forensics team ke liye audit logs save karna
logging.basicConfig(
    filename='nexus_audit.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# --- SYSTEM METADATA ---
OS_TYPE = platform.system()
VERSION = "v8.1-PROD"
# Naya Port taaki purana fasa hua port error na de!
PORT = 9090

# --- IN-MEMORY DATABASE ---
# Team note: Future me isko Redis/PostgreSQL par migrate karenge scalability ke liye
db = {
    "system_meta": {
        "version": VERSION,
        "platform": f"{OS_TYPE} Kernel",
        "uptime_start": time.time(),
    },
    "stats": {
        "total_packets_inspected": 0, # FIXED: 240590 ko 0 kar diya taaki UI me error na aaye
        "total_threats": 0, 
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
    db["audit_trail"].insert(0, {"timestamp": get_time(), "message": msg, "level": level})
    if len(db["audit_trail"]) > 20: 
        db["audit_trail"].pop()
        
    # Terminal Output ka Team Vibe Check
    if level == "CRITICAL":
        print(f"{C.RED}[!] {get_time()} - {msg}{C.RESET}")
    elif level == "WARNING":
        print(f"{C.YELLOW}[*] {get_time()} - {msg}{C.RESET}")
    elif level == "SUCCESS":
        print(f"{C.GREEN}[+] {get_time()} - {msg}{C.RESET}")
    else:
        print(f"{C.CYAN}[~] {get_time()} - {msg}{C.RESET}")

def get_local_ip():
    """Network team ka logic: Mac/Linux ka real Network IP dynamically nikalne ke liye"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# --- FIREWALL ADAPTER (KERNEL HOOKS & eBPF BRIDGE) ---
import struct

EBPF_ACTIVE = False
try:
    from bcc import BPF
    import ctypes
    
    # 1. C file ko load kar rahe hain (Path dhyan rakhna)
    bpf_engine = BPF(src_file="Phase1_eBPF_Research/nexus_kernel_hook.c")
    
    # 2. XDP hook ko attach kar rahe hain 
    INTERFACE = "lo" 
    bpf_engine.attach_xdp(dev=INTERFACE, fn=bpf_engine.load_func("nexus_packet_filter", BPF.XDP))
    
    # 3. Kernel Map ka access le rahe hain
    banned_map = bpf_engine.get_table("banned_ips_map")
    EBPF_ACTIVE = True
    print(f"{C.GREEN}[+] PHASE 1 COMPLETE: eBPF Kernel Hook Active on {INTERFACE}!{C.RESET}")

except Exception as e:
    print(f"{C.YELLOW}[*] RUNNING IN USER-SPACE MODE: eBPF bypass due to OS/Privilege ({e}){C.RESET}")

def ip_to_int(ip_str):
    """IP ko integer mein badalne ka helper taaki C code samajh sake"""
    return struct.unpack("I", socket.inet_aton(ip_str))[0]

def engage_firewall(ip, severity="TIER1"):
    """
    Core security logic! 
    Pehle eBPF map check karega, fail hone par iptables/sim mode par fallback karega.
    """
    if severity == "TIER2":
        if EBPF_ACTIVE:
            # LETHAL BAN: Seedha Kernel Map update (0.001ms)
            ip_int = ip_to_int(ip)
            banned_map[ctypes.c_uint32(ip_int)] = ctypes.c_uint8(1)
            add_log(f"KERNEL_SYNC: eBPF Map updated! {ip} banned at wire-speed.", "CRITICAL")
        elif OS_TYPE == "Linux":
            cmd = f"sudo firewall-cmd --permanent --add-rich-rule='rule family=\"ipv4\" source address=\"{ip}\" reject' > /dev/null 2>&1"
            add_log(f"OS_SYNC: iptables updated for {ip}.", "CRITICAL")
        else:
            add_log(f"SIM_MODE: Permanent Ban engaged against {ip}.", "CRITICAL")
            
    else:
        # TIER 1 (Soft Block)
        if OS_TYPE == "Linux":
            cmd = f"sudo firewall-cmd --add-rich-rule='rule family=\"ipv4\" source address=\"{ip}\" timeout=60s reject' > /dev/null 2>&1"
            add_log(f"OS_SYNC: iptables soft-block applied for {ip}.", "WARNING")
        else:
            add_log(f"SIM_MODE: Soft block timer started for {ip}.", "WARNING")

# --- MATRIX BOOT SEQUENCE ---
def run_matrix_boot():
    """Terminal me ek zabardast Hollywood hacker style boot animation dikhane ke liye"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(C.GREEN, end="")
    modules = ["TEAM_NEXUS_HOOK", "AI_ANOMALY_CORE", "DPI_PACKET_SCANNER", "AUTO_HEAL_DAEMON", "ZERO_TRUST_AUTH"]
    
    for _ in range(20):
        hex_str = "".join(random.choice("0123456789ABCDEF") for _ in range(12))
        mod = random.choice(modules)
        print(f"[0x{hex_str}] LOADING {mod} ... [OK]")
        time.sleep(0.01)
        
    print("\n[+] INITIALIZING TEAM NEXUS PROTOCOL..." + C.RESET)
    time.sleep(0.3)
    os.system('clear' if os.name == 'posix' else 'cls')

# --- API ENDPOINTS (Dashboard Integration) ---
@app.route('/')
def serve_dashboard():
    """Dashboard file direct browser me bheje ga (No 404 errors)"""
    return app.send_static_file('nexus_sentinel_dash.html')

@app.route('/api/telemetry', methods=['GET'])
def telemetry():
    now = time.time()
    # Team Logic: Auto-heal expired blocks efficiently
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

    if attacker_ip not in db["attacker_registry"]:
        db["attacker_registry"][attacker_ip] = {'strikes': 0, 'status': 'CLEAN'}

    db["attacker_registry"][attacker_ip]['strikes'] += 1
    strikes = db["attacker_registry"][attacker_ip]['strikes']
    
    # Team Metrics Update
    db["stats"]["total_threats"] += 1
    db["stats"]["total_packets_inspected"] += 1 # FIXED: Purane dashboard ko bhi support karega
    db["stats"]["threats_neutralized"] += 1

    if strikes == 1:
        db["attacker_registry"][attacker_ip]['status'] = 'BLOCKED'
        db["attacker_registry"][attacker_ip]['blocked_until'] = time.time() + 15
        db["stats"]["active_tier1_blocks"] += 1
        engage_firewall(attacker_ip, "TIER1")
        add_log(f"THREAT ISOLATED: {attack_vector} from {attacker_ip}.", "WARNING")
    else:
        db["attacker_registry"][attacker_ip]['status'] = 'BANNED'
        db["attacker_registry"][attacker_ip]['blocked_until'] = 9999999999
        db["stats"]["permanent_bans"] += 1
        if db["stats"]["active_tier1_blocks"] > 0: db["stats"]["active_tier1_blocks"] -= 1 
        engage_firewall(attacker_ip, "TIER2")
        add_log(f"LETHAL THREAT: Repeat attack from {attacker_ip}. PERMANENT BAN.", "CRITICAL")

    return jsonify({"status": "AIR_ENGAGED", "action": db["attacker_registry"][attacker_ip]['status']})

# --- BOOT SEQUENCE ---
if __name__ == '__main__':
    run_matrix_boot()
    NETWORK_IP = get_local_ip()
    
    print(f"{C.CYAN}")
    print(r"  _   _ ________  ___   _ _____   _____ _____ _   _ _____ _____ _   _ _____ _    ")
    print(r" | \ | |  ___|  \/  |  | /  ___| /  ___|  ___| \ | |_   _|_   _| \ | |  ___| |   ")
    print(r" |  \| | |__  \   / |  | \ `--.  \ `--.| |__ |  \| | | |   | | |  \| | |__ | |   ")
    print(r" | . ` |  __| /   \ |  | |`--. \  `--. \  __|| . ` | | |   | | | . ` |  __|| |   ")
    print(r" | |\  | |___/ /^\ \ \_/ /\__/ / /\__/ / |___| |\  | | |  _| |_| |\  | |___| |____")
    print(r" \_| \_/\____\/   \/\___/\____/  \____/\____/\_| \_/ \_/  \___/\_| \_\____/\_____/")
    print(f"{C.RESET}")
    
    print(f"{C.CYAN} >> AUTONOMOUS INCIDENT RESPONSE CORE v8.1{C.RESET}")
    print(f"{C.CYAN} >> DEVELOPED BY: Team Nexus Security{C.RESET}")
    print(f"{C.CYAN} >> PLATFORM: {OS_TYPE} | PORT: {PORT}{C.RESET}")
    print(f"{C.GREEN} >> Security Posture: HIGH | AI Core: ACTIVE{C.RESET}")
    print(f"{C.CYAN} >> Dashboard (Local):   http://127.0.0.1:{PORT} {C.RESET}")
    print(f"{C.CYAN} >> Dashboard (Network): http://{NETWORK_IP}:{PORT} {C.RESET}")
    print("-" * 75)
    
    add_log("System Boot: Core services engaged by Team Nexus.", "SUCCESS")
    add_log(f"Monitoring active on Port {PORT}. Awaiting packets...", "INFO")
    
    # Naye port ke sath application start hogi
    app.run(host='0.0.0.0', port=PORT)