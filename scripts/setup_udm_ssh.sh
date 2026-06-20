#!/bin/bash
# Setup SSH key on UDM using the BWS credentials
# Get the public key to add
echo "=== Our public key ==="
cat ~/.ssh/id_ed25519.pub

echo ""
echo "=== Testing SSH to UDM ==="
# Try different usernames
for user in root copilot admin; do
  echo "Trying $user..."
  sshpass -p "BUl1x3DVWHDD@$b" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$user@192.168.1.1" "echo 'Connected as $user'; uname -a; cat /etc/version 2>/dev/null || cat /etc/os-release 2>/dev/null | head -3" 2>&1
  if [ $? -eq 0 ]; then
    echo "SUCCESS with $user!"
    break
  fi
done