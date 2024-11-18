import os
import re
import subprocess

# Directory containing ovpn files
vpn_dir = './'

# List to store ovpn file names with responsive IPs
responsive_ovpn_files = []

# Function to extract IP address from ovpn file content
def extract_ip(ovpn_content):
    ip_pattern = re.compile(r'remote\s+([\d.]+)\s+\d+')
    match = ip_pattern.search(ovpn_content)
    if match:
        return match.group(1)
    return None

# Function to ping an IP address 15 times
def ping_ip(ip_address):
    command = ['ping', '-c', '15', ip_address]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        if ' 0% packet loss' in output:
            return True
    except subprocess.CalledProcessError:
        pass
    return False

# Scan ovpn files in the directory
for filename in os.listdir(ovpn_dir):
    if filename.endswith('.ovpn'):
        with open(os.path.join(ovpn_dir, filename), 'r') as file:
            ovpn_content = file.read()
            ip_address = extract_ip(ovpn_content)
            if ip_address and ping_ip(ip_address):
                responsive_ovpn_files.append(filename)

# Print the list of ovpn files with responsive IPs
print('Responsive ovpn files:', responsive_ovpn_files)
