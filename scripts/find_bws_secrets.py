#!/usr/bin/env python3
"""Try to get UDM SSH credentials from BWS"""
import json, subprocess, sys

# Try the bws Python library directly
sys.path.insert(0, '/home/alistair/.hermes/hermes-agent')

try:
    import bws
    print("bws module found:", dir(bws))
except ImportError:
    print("bws module not found")

# Try to find secrets in the installed bws package
r = subprocess.run(
    ['python3', '-m', 'bws', '--help'],
    capture_output=True, text=True, timeout=5
)
print("bws module help:", r.stdout[-500:])

# Check if there's a Hermes secrets interface
r2 = subprocess.run(
    ['find', '/home/alistair/.hermes/hermes-agent', '-name', '*secrets*', '-o', '-name', '*bitwarden*'],
    capture_output=True, text=True, timeout=10
)
print("\nHermes secrets files:")
for line in r2.stdout.split('\n'):
    if 'bitwarden' in line.lower() or 'secrets' in line.lower():
        print(f"  {line}")

# Try to list the bws package contents
r3 = subprocess.run(
    ['python3', '-c', 'import bws; print(bws.__file__)'],
    capture_output=True, text=True, timeout=5
)
print("\nbws location:", r3.stdout.strip())