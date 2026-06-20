#!/usr/bin/env python3
"""Copy SSH key to UDM - uses BWS for credentials"""
import pexpect, subprocess, sys, os, json

BWS = "/home/alistair/.hermes/bin/bws"

# Get credentials from BWS
r = subprocess.run(
    [BWS, "secret", "list", "cc3a84b5-96a4-4d09-8174-b45301870de2", "--output", "json"],
    capture_output=True, text=True, timeout=15
)
secrets = {s["key"]: s["value"] for s in json.loads(r.stdout)}

ssh_password = secrets.get("UNIFI_SSH_PASSWORD", "")
alt_password = secrets.get("UNIFI_PASSWORD", "")
username = secrets.get("UNIFI_USERNAME", "root")

# Read our public key
with open(os.path.expanduser("~/.ssh/id_ed25519.pub")) as f:
    pubkey = f.read().strip()

print("=== Public key ===")
print(pubkey)
print()

UDM = "192.168.1.1"
for pw in [ssh_password, alt_password]:
    for user in ["root", username, "admin"]:
        if not pw:
            continue
        print(f"Trying {user}@{UDM}...", end=" ", flush=True)
        try:
            child = pexpect.spawn(f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 {user}@{UDM}", timeout=15)
            i = child.expect(["assword:", "continue connecting", pexpect.EOF, pexpect.TIMEOUT])
            if i == 1:
                child.sendline("yes")
                i = child.expect(["assword:", pexpect.EOF, pexpect.TIMEOUT], timeout=10)
            if i == 0:
                child.sendline(pw)
                i2 = child.expect(["Permission denied", "#", r"\$", "assword:", pexpect.EOF, pexpect.TIMEOUT], timeout=5)
                if i2 in [1, 2]:  # # or $ prompt
                    print("✅ Connected!")
                    # Add SSH key
                    child.sendline(f"mkdir -p ~/.ssh && echo '{pubkey}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && chmod 700 ~/.ssh")
                    child.expect(["#", r"\$"], timeout=5)
                    child.sendline("echo KEY_OK")
                    child.expect("KEY_OK", timeout=5)
                    print("✅ SSH key installed!")
                    child.sendline("exit")
                    child.close()
                    # Test
                    print("\nTesting key-based auth...")
                    r = subprocess.run(
                        ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5",
                         f"{user}@{UDM}",
                         "uname -a; echo '---'; cat /etc/version 2>/dev/null || grep PRETTY /etc/os-release 2>/dev/null; echo '---'; df -h / | tail -1"],
                        capture_output=True, text=True, timeout=10
                    )
                    if r.returncode == 0:
                        print(f"✅ Key auth works for {user}!")
                        print(f"UDM Info: {r.stdout[:300]}")
                        sys.exit(0)
                elif i2 == 0:
                    print("❌ Denied")
                else:
                    print(f"Unexpected ({i2})")
            child.close()
        except Exception as e:
            print(f"Error: {e}")

print("\n❌ Could not connect")
sys.exit(1)