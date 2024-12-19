from data_fetcher import fetch_cve_data
from port_scanner import scan_network
from service_enumerator import grab_banner
from vuln_matcher import match_vulnerability
from ip_generator import generate_ips  # Import the function
import time

def select_region():
    print("[INFO] Please select a region:")
    print("1. North America")
    print("2. Europe")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        return "north_america"
    elif choice == "2":
        return "europe"
    else:
        print("[ERROR] Invalid selection. Please choose 1 or 2.")
        return select_region()


def main():
    region = select_region()
    print(f"[INFO] Selected Region: {region.replace('_', ' ').title()}")

    # Generate 10 random IPs for the selected region, pingable ones
    print(f"[INFO] Generating 10 random IPs for {region.replace('_', ' ').title()}...")
    ip_list = generate_ips(region, 10)

    if not ip_list:
        print("[ERROR] No reachable IPs found. Exiting.")
        return

    print(f"[INFO] {len(ip_list)} reachable IP(s) found.")

    print("[STEP 1] Fetching CVE Data...")
    fetch_cve_data()

    print("[STEP 2] Scanning Network...")
    for ip in ip_list:
        print(f"[INFO] Scanning IP: {ip}")  # Print the current IP being scanned
        scan_results = scan_network(ip)
        time.sleep(0.5)

        print("[STEP 3] Enumerating Services...")
        for result in scan_results:
            banner = grab_banner(result["host"], result["port"])
            print(f"Banner for {result['host']}:{result['port']} -> {banner}")
            time.sleep(0.2)
            print("[STEP 4] Matching Vulnerabilities...")
            matches = match_vulnerability(result["service"], result["version"])
            if matches:
                for match in matches:
                    print(f"Vulnerability Found: {match['id']} - {match['description']}")

if __name__ == "__main__":
    main()
