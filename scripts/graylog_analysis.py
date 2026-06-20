#!/usr/bin/env python3
"""Graylog UniFi data analysis"""
import subprocess, json, re, csv, io
from urllib.parse import quote

SESSION = "856be757-06b9-45d8-8429-108faf1902ec"
AUTH = "Cookie: authentication=" + SESSION
BASE = "http://192.168.1.124:9009/api"

def gl_search(query, fields="message,source,timestamp", limit=1000, range_sec=172800):
    url = f"{BASE}/search/universal/relative?query={quote(query)}&range={range_sec}&limit={limit}&fields={fields}"
    r = subprocess.run(
        ["curl", "-s", url, "-H", AUTH, "-H", "X-Requested-By: hermes"],
        capture_output=True, text=True, timeout=120
    )
    return r.stdout

# ===== 1. OVERVIEW =====
print("=" * 60)
print("GRAYLOG UNIFI DATA ANALYSIS")
print("= services VM (192.168.1.124) =")
print("=" * 60)

# Total CEF messages
cef_48h = gl_search("CEF:0", "message", 50000, 172800)
cef_lines = [l for l in cef_48h.split("\n") if l.strip() and "CEF:0" in l]
print(f"\nTotal CEF messages (48h): {len(cef_lines)}")

cef_7d = gl_search("CEF:0", "message", 50000, 604800)
cef_7d_lines = [l for l in cef_7d.split("\n") if l.strip() and "CEF:0" in l]
print(f"Total CEF messages (7d): {len(cef_7d_lines)}")

# ===== 2. THREAT EVENTS =====
print(f"\n{'='*60}")
print("THREAT DETECTED AND BLOCKED")
print(f"{'='*60}")

threat = gl_search("message:%22Threat+Detected%22", "message", 5000, 172800)
threat_lines = [l for l in threat.split("\n") if l.strip() and "CEF:0" in l]
print(f"Threat Detected events (48h): {len(threat_lines)}")

# ===== 3. CATEGORY BREAKDOWN =====
print(f"\n{'='*60}")
print("EVENT CATEGORY BREAKDOWN (48h)")
print(f"{'='*60}")

def extract_event_name(msg):
    """Extract the event name from CEF format"""
    # CEF:0|Vendor|Product|Version|EventID|Name|Severity|
    m = re.search(r'CEF:0\|[^|]+\|[^|]+\|[^|]+\|(\d+)\|([^|]+)\|(\d+)\|', msg)
    if m:
        return m.group(2)
    return "Unknown"

categories = {}
for l in cef_lines:
    # Extract the message field (second quoted field)
    parts = l.split('","')
    msg = parts[1] if len(parts) > 1 else l
    name = extract_event_name(msg)
    categories[name] = categories.get(name, 0) + 1

for name, count in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"  {count:>5}  {name}")

# ===== 4. THREAT SIGNATURE BREAKDOWN =====
print(f"\n{'='*60}")
print("THREAT SIGNATURES / IPS CATEGORIES")
print(f"{'='*60}")

threat_sigs = {}
for l in threat_lines:
    parts = l.split('","')
    msg = parts[1] if len(parts) > 1 else l
    # Extract UNIFI category
    cat_m = re.search(r'UNIFIcategory=([^\s]+)', msg)
    sig_m = re.search(r'UNIFIipsSignature=([^\s]+)', msg)
    cat = cat_m.group(1) if cat_m else "Unknown"
    sig = sig_m.group(1) if sig_m else "Unknown"
    key = f"{cat} / {sig}"
    threat_sigs[key] = threat_sigs.get(key, 0) + 1

for sig, count in sorted(threat_sigs.items(), key=lambda x: -x[1]):
    print(f"  {count:>5}  {sig}")

# ===== 5. SAMPLE THREAT MESSAGES =====
print(f"\n{'='*60}")
print("SAMPLE THREAT EVENTS")
print(f"{'='*60}")
for l in threat_lines[:5]:
    parts = l.split('","')
    msg = parts[1] if len(parts) > 1 else l
    # Extract key fields
    fields = {
        'src': re.search(r'src=([^\s]+)', msg),
        'dst': re.search(r'dst=([^\s]+)', msg),
        'dpt': re.search(r'dpt=(\d+)', msg),
        'proto': re.search(r'proto=([^\s]+)', msg),
        'act': re.search(r'act=([^\s]+)', msg),
        'cat': re.search(r'UNIFIcategory=([^\s]+)', msg),
        'sig': re.search(r'UNIFIipsSignature=([^\s]+)', msg),
        'risk': re.search(r'UNIFIrisk=([^\s]+)', msg),
    }
    print(f"  Event: {extract_event_name(msg)}")
    for k, v in fields.items():
        if v:
            print(f"    {k}: {v.group(1)}")
    print()

# ===== 6. TOP TALKERS =====
print(f"{'='*60}")
print("TOP ATTACKING SOURCE IPs (48h)")
print(f"{'='*60}")

src_ips = {}
dst_ips = {}
for l in threat_lines:
    parts = l.split('","')
    msg = parts[1] if len(parts) > 1 else l
    src_m = re.search(r'src=([^\s]+)', msg)
    dst_m = re.search(r'dst=([^\s]+)', msg)
    if src_m:
        ip = src_m.group(1)
        src_ips[ip] = src_ips.get(ip, 0) + 1
    if dst_m:
        ip = dst_m.group(1)
        dst_ips[ip] = dst_ips.get(ip, 0) + 1

print("Source IPs (attackers):")
for ip, count in sorted(src_ips.items(), key=lambda x: -x[1])[:10]:
    print(f"  {count:>5}  {ip}")

print("\nDestination IPs (targets):")
for ip, count in sorted(dst_ips.items(), key=lambda x: -x[1])[:10]:
    print(f"  {count:>5}  {ip}")

# ===== 7. CLIENT ACTIVITY =====
print(f"\n{'='*60}")
print("CLIENT CONNECT/DISCONNECT ACTIVITY (48h)")
print(f"{'='*60}")

clients = {}
for l in cef_lines:
    parts = l.split('","')
    msg = parts[1] if len(parts) > 1 else l
    host_m = re.search(r'UNIFIclientHostname=([^\s]+)', msg)
    ip_m = re.search(r'UNIFIclientIp=([^\s]+)', msg)
    if host_m:
        name = host_m.group(1)
        ip = ip_m.group(1) if ip_m else "?"
        clients[name] = clients.get(name, 0) + 1

for name, count in sorted(clients.items(), key=lambda x: -x[1])[:10]:
    print(f"  {count:>5}  {name}")

print(f"\n{'='*60}")
print("DONE")