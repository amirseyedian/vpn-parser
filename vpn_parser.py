import os
import re
import subprocess
from tqdm import tqdm
import tempfile

# Directory containing ovpn files
ovpn_dir = './'

# User credentials
username = 'openvpnusername'
password = 'openvpnpassword'

# List to store tuples of (ovpn file name, IP address)
ovpn_ip_list = []

# List to store ovpn file names that successfully connected
successful_connections = []

# Function to extract IP address from ovpn file content
def extract_ip(ovpn_content):
    ip_pattern = re.compile(r'remote\s+([\d.]+)\s+\d+')
    match = ip_pattern.search(ovpn_content)
    if match:
        return match.group(1)
    return None

# Function to attempt OpenVPN connection
def attempt_openvpn_connection(ovpn_file, credentials_file):
    command = ['sudo', 'openvpn', '--config', ovpn_file, '--auth-user-pass', credentials_file, '--connect-timeout', '10']
    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, timeout=30)
        return True
    except subprocess.CalledProcessError:
        pass
    except subprocess.TimeoutExpired:
        pass
    return False

# Create a temporary file to store credentials
with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as cred_file:
    cred_file.write(f'{username}\n{password}\n')
    credentials_file = cred_file.name

# Read ovpn files and save IP addresses with corresponding file names
for filename in tqdm(os.listdir(ovpn_dir), desc="Reading ovpn files", unit="file"):
    if filename.endswith('.ovpn'):
        with open(os.path.join(ovpn_dir, filename), 'r') as file:
            ovpn_content = file.read()
            ip_address = extract_ip(ovpn_content)
            if ip_address:
                ovpn_ip_list.append((filename, ip_address))

# Attempt to connect to VPNs and save successful connections
for ovpn_file, ip_address in tqdm(ovpn_ip_list, desc="Connecting to VPNs", unit="vpn"):
    ovpn_file_path = os.path.join(ovpn_dir, ovpn_file)
    if attempt_openvpn_connection(ovpn_file_path, credentials_file):
        successful_connections.append(ovpn_file)

# Delete the temporary credentials file
os.unlink(credentials_file)

# Print the list of ovpn files that successfully connected
print('Successfully connected to VPNs:')
for ovpn_file in successful_connections:
    print(ovpn_file)
