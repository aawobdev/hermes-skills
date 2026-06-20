#!/usr/bin/env python3
"""Graylog UniFi data analysis - extended"""
import subprocess, re

SESSION = "856be757-06b9-45d8-8429-108faf1902ec"
AUTH = 'Cookie: authentication=%s' % SESSION

def gl(query, fields="message,source,timestamp", limit=50000, r=172800):
    url = "http://192.168.1.124:9009/api/search/universal/relative?query=%s&range=%d&limit=%d&fields=%s" % (query, r, limit, fields)
    r = subprocess.run(
        ["curl", "-s", url, "-H", AUTH, "-H", "X-Requested-By: hermes"],
        capture_output=True, text=True, timeout=120
    )
    return r.stdout

print("=== TOTAL VOLUME BY TIME PERIOD ===")
for hours, label in [(3600, "1h"), (7200, "2h"), (21600, "6h"), (43200, "12h"), (86400, "24h"), (172800, "48h"), (604800, "7d")]:
    raw = gl("Threat+Detected", "message", 50000, hours)
    ct = len([l for l in raw.split("\n") if l.strip() and "CEF:0" in l])
    print("  %s: %d threat events" % (label, ct))

print()
print("=== THREATS BY PROTOCOL ===")
raw = gl("Threat+Detected", "message", 5000, 172800)
threat_lines = [l for l in raw.split("\n") if l.strip() and "CEF:0" in l]
print("Total threats (48h): %d" % len(threat_lines))

protos = {}
dports = {}
for l in threat_lines:
    pm = re.search(r'proto=(\S+)', l)
    dm = re.search(r'dpt=(\S+)', l)
    if pm: protos[pm.group(1)] = protos.get(pm.group(1), 0) + 1
    if dm: dports[dm.group(1)] = dports.get(dm.group(1), 0) + 1

print("Protocol:")
for p, c in sorted(protos.items(), key=lambda x: -x[1]):
    print("  %s: %d (%d%%)" % (p, c, c*100//len(threat_lines)))
print("Top destination ports:")
for p, c in sorted(dports.items(), key=lambda x: -x[1])[:10]:
    print("  %s: %d" % (p, c))

print()
print("=== TOP DESTINATION IPs (external targets) ===")
dst_ips = {}
for l in threat_lines:
    m = re.search(r'dst=(\S+)', l)
    if m:
        ip = m.group(1)
        dst_ips[ip] = dst_ips.get(ip, 0) + 1
for ip, c in sorted(dst_ips.items(), key=lambda x: -x[1])[:15]:
    print("  %5d  %s" % (c, ip))

print()
print("=== TOP SOURCE IPs (external attackers when present) ===")
src_ips = {}
for l in threat_lines:
    m = re.search(r'src=(\S+)', l)
    if m:
        ip = m.group(1)
        src_ips[ip] = src_ips.get(ip, 0) + 1
print("Total threats with source_ip: %d / %d" % (sum(src_ips.values()), len(threat_lines)))
for ip, c in sorted(src_ips.items(), key=lambda x: -x[1])[:15]:
    print("  %5d  %s" % (c, ip))

print()
print("=== INTERNAL DEVICE HOSTNAMES ===")
clients = {}
for l in threat_lines:
    m = re.search(r'UNIFIsrcClientHostname=([^\s]+)', l)
    if m:
        clients[m.group(1)] = clients.get(m.group(1), 0) + 1
# Also try UNIFIclientAlias
for l in threat_lines:
    m = re.search(r'UNIFIclientAlias=([^\\s]+)', l)
    if m and m.group(1) not in clients:
        alias = m.group(1)
        # Clean up
        alias = alias.strip()
        if alias:
            clients[alias] = clients.get(alias, 0) + 1
if clients:
    for name, c in sorted(clients.items(), key=lambda x: -x[1])[:10]:
        print("  %5d  %s" % (c, name))
else:
    print("  No client hostnames found in threat events")

print()
print("=== INTERNAL IPs (targeted internal devices) ===")
int_ips = {}
for l in threat_lines:
    m = re.search(r'dst=192\.168\.([^\s]+)', l)
    if m:
        ip = "192.168." + m.group(1)
        int_ips[ip] = int_ips.get(ip, 0) + 1
for ip, c in sorted(int_ips.items(), key=lambda x: -x[1]):
    print("  %5d  %s" % (c, ip))

print()
print("=== IPS SIGNATURE RULES ===")
sigs = {}
for l in threat_lines:
    m = re.search(r'UNIFIipsSignature=([^\s]+)', l)
    if m:
        s = m.group(1)
        sigs[s] = sigs.get(s, 0) + 1
for s, c in sorted(sigs.items(), key=lambda x: -x[1])[:15]:
    print("  %5d  %s" % (c, s))

print()
print("=== RISK LEVELS ===")
risks = {}
for l in threat_lines:
    m = re.search(r'UNIFIrisk=([^\s]+)', l)
    if m:
        r = m.group(1)
        risks[r] = risks.get(r, 0) + 1
for r, c in sorted(risks.items(), key=lambda x: -x[1]):
    print("  %5d  %s" % (c, r))

print()
print("=== ALL CEF EVENT TYPES (48h) ===")
raw = gl("CEF", "message", 50000, 172800)
all_cef = [l for l in raw.split("\n") if l.strip() and "CEF:0" in l]
cats = {}
for l in all_cef:
    m = re.search(r'CEF:0\|[^|]+\|[^|]+\|[^|]+\|\d+\|([^|]+)\|', l)
    if m:
        n = m.group(1)
        cats[n] = cats.get(n, 0) + 1
for n, c in sorted(cats.items(), key=lambda x: -x[1])[:20]:
    print("  %5d  %s" % (c, n))
if all_cef:
    print()
    print("Total CEF messages (48h): %d" % len(all_cef))

print()
print("=== DONE ===")
