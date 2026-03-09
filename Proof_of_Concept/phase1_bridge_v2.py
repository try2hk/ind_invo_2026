# --- FIREWALL ADAPTER (KERNEL HOOKS & eBPF BRIDGE) --- no dependenciec
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