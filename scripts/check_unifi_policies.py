#!/usr/bin/env python3
"""Check UniFi firewall policies via API"""
import subprocess, json, sys

# Get creds
r = subprocess.run(
    ["/home/alistair/.hermes/bin/bws", "secret", "list", "cc3a84b5-96a4-4d09-8174-b45301870de2", "--output", "json"],
    capture_output=True, text=True, timeout=15
)
secrets = {s["key"]: s["value"] for s in json.loads(r.stdout)}
pwd = secrets.get("UNIFI_PASSWORD", "")

# Login - store cookies
subprocess.run(
    ["curl", "-sk", "-X", "POST", "https://192.168.1.1/api/auth/login",
     "-H", "Content-Type: application/json",
     "-d", '{"username":"copilot","password":"%s"}' % pwd,
     "-c", "/tmp/unifi_cookies.txt"],
    capture_output=True, text=True, timeout=15
)

# Read cookies
headers = ["-H", "Content-Type: application/json", "-b", "/tmp/unifi_cookies.txt"]

# Check what policies exist
r2 = subprocess.run(["curl", "-sk", "https://192.168.1.1/api/v2/firewall/policies"] + headers,
    capture_output=True, text=True, timeout=15)
print("=== POLICIES ===")
try:
    parsed = json.loads(r2.stdout)
    print(json.dumps(parsed, indent=2)[:3000])
except:
    print(r2.stdout[:2000])

# Port forwarding  
r3 = subprocess.run(["curl", "-sk", "https://192.168.1.1/proxy/network/api/s/default/rest/portforward"] + headers,
    capture_output=True, text=True, timeout=15)
print("\n=== PORT FORWARD ===")
try:
    parsed3 = json.loads(r3.stdout)
    print(json.dumps(parsed3, indent=2)[:3000])
except:
    print(r3.stdout[:2000])