#!/usr/bin/env python3
"""Cross-ref Graylog threats with Plex user IPs"""
import subprocess, re, json
from collections import defaultdict

# ===== PART 1: Get Plex log IPs from media VM =====
r = subprocess.run([
    'ssh', 'media',
    r"grep -r -h -E '(Remote Public Address|client.*ip|from.*[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+|User.*authenticated|authorized)' "
    "'/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.log' "
    "'/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.1.log' "
    "'/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.2.log' "
    "'/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.3.log' "
    "'/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.4.log' "
    "2>/dev/null | tail -50",
], capture_output=True, text=True, timeout=30)
print("=== PLEX AUTH/ACCESS LOGS ===")
print(r.stdout[-2000:])

# ===== PART 2: Get all external IPs from Plex logs =====
r2 = subprocess.run([
    'ssh', 'media',
    r"grep -r -h -oP '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' "
    "'/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.log' "
    "'/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.1.log' "
    "'/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.2.log' "
    "'/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.3.log' "
    "'/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.4.log' "
    "2>/dev/null | sort -u | grep -v '^192\.168\.\|^127\.\|^0\.0\.0\.0\|^172\.\(17\|18\|19\)\.\|^169\.254\.'",
], capture_output=True, text=True, timeout=30)

plex_external_ips = set(r2.stdout.strip().split('\n'))
print()
print("=== EXTERNAL IPs FOUND IN PLEX LOGS ===")
for ip in sorted(plex_external_ips):
    if ip:
        print(f"  {ip}")

# ===== PART 3: Inbound threat IPs from Graylog =====
threat_ips_inbound = {
    '66.132.172.220': 4,
    '168.222.241.36': 2,
    '195.47.238.50': 2,
    '1.2.3.4': 2,
    '45.41.207.167': 2,
    '23.137.105.248': 2,
    '107.172.127.242': 2,
    '8.8.8.8': 1,
    '27.100.36.17': 1,
    '151.242.242.143': 1,
    '115.187.16.42': 1,
    '185.55.240.168': 1,
    '149.202.85.99': 1,
    '195.72.60.53': 1,
    '151.242.242.39': 1,
}

print()
print("=" * 70)
print("CROSS-REFERENCE: Graylog threats vs Plex user IPs")
print("=" * 70)

plex_known_ips = set()
for ip in plex_external_ips:
    if ip:
        ip = ip.strip()
        if ip:
            plex_known_ips.add(ip)

print(f"\nUnique external IPs in Plex logs: {len(plex_known_ips)}")
print(f"Inbound threat IPs (Graylog): {len(threat_ips_inbound)}")

# Check for any overlaps
overlap = set(threat_ips_inbound.keys()) & plex_known_ips
if overlap:
    print(f"\n🚨 OVERLAP FOUND! {len(overlap)} IPs are BOTH in Plex logs AND threat data:")
    for ip in sorted(overlap):
        print(f"  {ip} appeared {threat_ips_inbound[ip]} times in threats")
else:
    print(f"\n✅ No direct overlap - the inbound threat IPs are NOT known Plex users")

# Check for subnet overlaps
print(f"\n=== SUBNET ANALYSIS ===")
threat_subnets = defaultdict(set)
for ip in threat_ips_inbound:
    parts = ip.split('.')
    if len(parts) == 4:
        threat_subnets['.'.join(parts[:3])].add(ip)

plex_subnets = defaultdict(set)
for ip in plex_known_ips:
    parts = ip.split('.')
    if len(parts) == 4:
        plex_subnets['.'.join(parts[:3])].add(ip)

# Check if any threat subnet overlaps with Plex subnets
for subnet, threat_ips in sorted(threat_subnets.items()):
    plex_ips_in_subnet = plex_subnets.get(subnet, set())
    if plex_ips_in_subnet:
        print(f"Overlap in subnet {subnet}.x:")
        print(f"  Threat IPs: {', '.join(sorted(threat_ips))}")
        print(f"  Plex IPs: {', '.join(sorted(plex_ips_in_subnet))}")
    else:
        for tip in threat_ips:
            print(f"  {tip} - no known Plex activity in subnet")

# ===== PART 4: List Plex user IPs grouped by user =====
print(f"\n{'='*70}")
print("PLEX USERS vs IP ADDRESSES")
print("(Need Plex token to map log IPs to usernames)")
print(f"{'='*70}")

print(f"\nKnown Plex users shared with:")
print(f"  alis719 (you - admin)")
print(f"  SeregonZA")
print(f"  bluema90")
print(f"  kellyem")
print(f"  Craig Schwegmann")
print(f"  al5608")
print(f"  aprob13")
print(f"  pen657")

print(f"\nExternal IPs in Plex logs that are LIKELY users (non-scanning):")
likely_user_ips = [ip for ip in sorted(plex_known_ips) if ip and not ip.startswith('167.94.') and not ip.startswith('66.132.172.')]
for ip in likely_user_ips:
    # Attempt GeoIP lookup
    try:
        r = subprocess.run(['geoiplookup', ip], capture_output=True, text=True, timeout=5)
        geo = r.stdout.strip()[:80] if r.stdout else 'Unknown'
    except:
        geo = '(geo lookup unavailable)'
    print(f"  {ip:<20} {geo}")

print(f"\nPassive scanner IPs (likely not users):")
scanner_ips = [ip for ip in sorted(plex_known_ips) if ip.startswith('167.94.') or ip.startswith('66.132.172.')]
for ip in scanner_ips:
    print(f"  {ip}")