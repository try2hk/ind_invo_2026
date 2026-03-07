# Iske liye server pe 'bcc' library install honi chahiye
from bcc import BPF
import socket
import struct
import ctypes

# 1. Load the eBPF C program that you already wrote
# (Ye line aapke C code ko kernel space mein compile aur load karti hai)
bpf_engine = BPF(src_file="../Phase1_eBPF_Research/nexus_kernel_hook.c")

# 2. Attach it to the Network Interface (e.g., eth0 ya wlan0)
# (Demo ke liye interface ka naam apne system ke hisaab se change kar lena)
interface = "eth0" 
bpf_engine.attach_xdp(dev=interface, fn=bpf_engine.load_func("nexus_packet_filter", BPF.XDP))

# 3. Access the BPF Map directly from Python
# (Ye wahi map hai jo aapne C code mein 'banned_ips_map' naam se banaya tha)
banned_map = bpf_engine.get_table("banned_ips_map")

def ip_to_int(ip_str):
    """IP string ko Network Byte Order (Integer) mein convert karta hai jo C code samajhta hai"""
    return struct.unpack("I", socket.inet_aton(ip_str))[0]

def engage_firewall(ip, severity="TIER1"):
    """
    UPGRADED CORE LOGIC (PHASE 1 COMPLETE):
    Ab hum iptables/firewalld use nahi kar rahe, seedha Kernel mem-map update kar rahe hain!
    """
    ip_int = ip_to_int(ip)
    
    if severity == "TIER2":
        # Autonomous Lethal Ban: Map mein value '1' set karte hi C code packet drop karna shuru kar dega (0.001ms)
        banned_map[ctypes.c_uint32(ip_int)] = ctypes.c_uint8(1)
        add_log(f"eBPF KERNEL SYNC: {ip} permanently banned at wire-speed.", "CRITICAL")
    else:
        # Tier 1 ke liye aap temporary logic ya eBPF map mein ek alag value (e.g., 2) set kar sakte hain
        add_log(f"SIM_MODE: Soft block engaged against {ip}.", "WARNING")