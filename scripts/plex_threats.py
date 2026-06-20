#!/usr/bin/env python3
"""Get Plex 32400 threat events"""
import subprocess, re

url = 'http://192.168.1.124:9009/api/search/universal/relative?query=message:dpt=32400&range=604800&limit=100&fields=message,source,timestamp'
auth = 'Cookie: authentication=856be757-06b9-45d8-8429-108faf1902ec'

r = subprocess.run(
    ['curl', '-s', url, '-H', auth, '-H', 'X-Requested-By: hermes'],
    capture_output=True, text=True, timeout=30
)

lines = [l for l in r.stdout.split('\n') if l.strip() and 'CEF:0' in l]
print(f'Total threat hits on port 32400 (7d): {len(lines)}')
print()

for l in lines:
    parts = l.split('","')
    msg = parts[1] if len(parts) > 1 else parts[0]
    ts = parts[0].strip('"') if len(parts) > 1 else '?'
    
    src = re.search(r'src=([^\s]+)', msg)
    dst = re.search(r'dst=([^\s]+)', msg)
    act = re.search(r'act=([^\s]+)', msg)
    sig = re.search(r'UNIFIipsSignature=([^\s]+)', msg)
    risk = re.search(r'UNIFIrisk=([^\s]+)', msg)
    
    print(f'  [{ts}]')
    print(f'    src={src.group(1) if src else "?"}  dst={dst.group(1) if dst else "?"}')
    print(f'    action={act.group(1) if act else "?"}  sig={sig.group(1) if sig else "?"}  risk={risk.group(1) if risk else "?"}')
    print()