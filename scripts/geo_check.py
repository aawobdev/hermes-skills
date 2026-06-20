#!/usr/bin/env python3
"""Get GeoIP/ASN data from Graylog for key IPs"""
import subprocess, re

auth_header = "Cookie: authentication=856be757-06b9-45d8-8429-108faf1902ec"

def gl_search(query, limit=10, fields="message"):
    url = "http://192.168.1.124:9009/api/search/universal/relative?query=%s&range=604800&limit=%d&fields=%s" % (query, limit, fields)
    r = subprocess.run(['curl', '-s', url, '-H', auth_header, '-H', 'X-Requested-By: hermes'], capture_output=True, text=True, timeout=15)
    return [l for l in r.stdout.split('\n') if l.strip() and 'CEF:0' in l]

print("=== Threat IP 66.132.172.220 (source/destination context) ===")
for l in gl_search("message:66.132.172.220", 5):
    print(l[:400])
    print()

print("=== Plex log IPs (likely scanners) ===")
for ip in ['167.94.146.54', '167.94.146.58']:
    lines = gl_search("message:" + ip, 3)
    if lines:
        print("%s: %d hits" % (ip, len(lines)))
        for l in lines[:2]:
            print(l[:300])
    else:
        print("%s: no hits in Graylog" % ip)

print()
print("=== Interesting Plex external IPs (likely actual users) ===")
for ip in ['147.12.191.17', '178.79.179.11', '2.221.110.222', '102.182.160.78']:
    lines = gl_search("message:" + ip, 3)
    if lines:
        print("%s: FOUND (%d hits)" % (ip, len(lines)))
        for l in lines[:1]:
            print("  " + l[:200])
    else:
        print("%s: not in Graylog" % ip)