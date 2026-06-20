#!/usr/bin/env python3
"""Cross-reference inbound threats with Plex user data"""
import subprocess, re, json

# ===== PART 1: Get all inbound threats to Plex server =====
url = 'http://192.168.1.124:9009/api/search/universal/relative?query=message:dst=192.168.1.206&range=604800&limit=100&fields=message,source,timestamp'
auth = 'Cookie: authentication=856be757-06b9-45d8-8429-108faf1902ec'

r = subprocess.run(
    ['curl', '-s', url, '-H', auth, '-H', 'X-Requested-By: hermes'],
    capture_output=True, text=True, timeout=30
)

lines = [l for l in r.stdout.split('\n') if l.strip() and 'CEF:0' in l]
print('=' * 70)
print('INBOUND THREATS TARGETING PLEX SERVER (192.168.1.206:32400)')
print('=' * 70)
print(f'Total: {len(lines)} threats in 7 days')
print()

inbound_ips = set()
for l in lines:
    parts = l.split('","')
    msg = parts[1] if len(parts) > 1 else parts[0]
    ts = parts[0].strip('"') if len(parts) > 1 else '?'
    
    src = re.search(r'src=([^\s]+)', msg)
    dst = re.search(r'dst=([^\s]+)', msg)
    act = re.search(r'act=([^\s]+)', msg)
    
    src_ip = src.group(1) if src else '?'
    dst_ip = dst.group(1) if dst else '?'
    if src_ip != '?':
        inbound_ips.add(src_ip)
    
    print(f'  [{ts}] {src_ip:>16} -> {dst_ip:>16}  ({act.group(1) if act else "?"})')

print()
print(f'Unique external IPs probing Plex: {len(inbound_ips)}')
for ip in sorted(inbound_ips):
    print(f'  - {ip}')

# ===== PART 2: Check if Plex is accessible =====
print()
print('=' * 70)
print('ATTEMPTING PLEX API ACCESS')
print('=' * 70)

# Check what's on the media VM
subprocess.run(['ssh', 'media', 'which plex-media-server || systemctl is-active plexmediaserver 2>/dev/null || docker ps --filter name=plex --format "{{.Names}} {{.Status}}"'], timeout=15)
