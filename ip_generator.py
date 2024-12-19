import random
import ipaddress
import subprocess
from tqdm import tqdm  # Progress bar library
import itertools

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


def ping_ip(ip):
    """
    Pings an IP address to check if it is reachable.
    Returns True if the IP is reachable, False otherwise.
    """
    try:
        response = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return response.returncode == 0
    except Exception:
        return False


def generate_ips(region, num_ips=10):
    """
    Generates a list of random reachable IPs from the selected region's IP ranges.
    Only returns IPs that are reachable (pingable).
    Displays a progress bar while generating and pinging the IPs.
    """
    reachable_ips = []
    networks = [ipaddress.ip_network(cidr) for cidr in IP_RANGES.get(region, [])]

    # Progress bar setup
    with tqdm(total=num_ips, desc="Generating Pingable IPs", unit="IP", ncols=80, dynamic_ncols=True) as pbar:
        for _ in itertools.count():
            # Select a random network and generate a random IP within it
            network = random.choice(networks)
            random_ip = str(ipaddress.IPv4Address(random.randint(int(network.network_address), int(network.broadcast_address))))

            # Overwrite the line with the current IP being checked


            # Ping the IP and check if it's reachable
            if ping_ip(random_ip):
                reachable_ips.append(random_ip)
                pbar.update(1)  # Update the progress bar after finding each reachable IP

            if len(reachable_ips) >= num_ips:
                print()  # End the "Checking IP" line
                break

    return reachable_ips


