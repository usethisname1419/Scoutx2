import random
import ipaddress
import subprocess
from tqdm import tqdm  # Progress bar library
import itertools
from logger import print_error
# IP ranges for North America and Europe
IP_RANGES = {
    "north_america": [
        "194.149.76.0/24",
        "185.203.206.0/24",
        "185.204.185.0/24",
        "193.39.184.0/22"
    ],
    "europe": [
        "193.36.132.0/24",
        "193.34.32.0/22",
        "193.32.93.0/24",
        "193.31.254.0/23"
    ]
}


def ping_ip(ip, os_type="windows"):
    """
    Pings an IP address to check if it is reachable.
    Returns True if the IP is reachable, False otherwise.
    Uses -n for Windows and -c for Linux.
    
    """
    try:
        ping_command = ['ping', '-n', '1', ip] if os_type.lower() == "windows" else ['ping', '-c', '1', ip]
        response = subprocess.run(ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return response.returncode == 0
    except Exception as e:
        print_error(f"Failed to ping {ip}: {e}")
        return False



def generate_ips(region, num_ips=10, os_type="windows"):
    """
    Generates a list of random reachable IPs from the selected region's IP ranges.
    Only returns IPs that are reachable (pingable).
    Displays a progress bar while generating and pinging the IPs.
    Does not allow for generating more than 100, To reduce abuse.
    """
    if num_ips > 100:
        print_error("Cannot generate more than 100 IPs.")
        raise ValueError()

    reachable_ips = []
    networks = [ipaddress.ip_network(cidr) for cidr in IP_RANGES.get(region, [])]

    with tqdm(total=num_ips, desc="Generating Pingable IPs", unit="IP", ncols=80, dynamic_ncols=True) as pbar:
        for _ in itertools.count():
            network = random.choice(networks)
            random_ip = str(ipaddress.IPv4Address(random.randint(
                int(network.network_address), int(network.broadcast_address))))

            if ping_ip(random_ip, os_type):
                reachable_ips.append(random_ip)
                pbar.update(1)

            if len(reachable_ips) >= num_ips:
                break

    return reachable_ips



