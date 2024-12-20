from data_fetcher import fetch_cve_data
from port_scanner import scan_network
from service_enumerator import grab_banner
from vuln_matcher import match_vulnerability
from ip_generator import generate_ips
import time
import logger
from colorama import Fore, Style, init
from logger import print_info, print_error, print_step
# Initialize colorama
init(autoreset=True)


def title():
    """
    Displays the title screen with ASCII art and branding information.
    """
     art = r"""
 
 
 $$$$$$\                                  $$\                      $$$$$$\  
$$  __$$\                                 $$ |                    $$  __$$\ 
$$ /  \__| $$$$$$$\  $$$$$$\  $$\   $$\ $$$$$$\                   \__/  $$ |
\$$$$$$\  $$  _____|$$  __$$\ $$ |  $$ |\_$$  _|                   $$$$$$  |
 \____$$\ $$ /      $$ /  $$ |$$ |  $$ |  $$ |                    $$  ____/ 
$$\   $$ |$$ |      $$ |  $$ |$$ |  $$ |  $$ |$$\      \\//       $$ |      
\$$$$$$  |\$$$$$$$\ \$$$$$$  |\$$$$$$  |  \$$$$  |     //\\       $$$$$$$$\ 
 \______/  \_______| \______/  \______/    \____/                 \________|
                                                                              
                                                                                                                                                       
       Powered by LTH Cybersecurity
    """
    print(art)




def select_scan_type():
    """
    Allows the user to select between a local or regional scan.
    """
    print_info("Select scan type:")
    print("1. Local Scan (127.0.0.1)")
    print("2. Regional Scan")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        return "local"
    elif choice == "2":
        return "regional"
    else:
        print_error("Invalid selection. Please choose 1 or 2.")
        return select_scan_type()


def select_region():
    """
    Allows the user to select a region for scanning.
    """
    print_info("Please select a region:")
    print("1. North America")
    print("2. Europe")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        return "north_america"
    elif choice == "2":
        return "europe"
    else:
        print_error("Invalid selection. Please choose 1 or 2.")
        return select_region()


def select_os():
    """
    Allows the user to select their operating system for ping functionality.
    """
    print_info("Please select your operating system:")
    print("1. Windows")
    print("2. Linux")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        return "windows"
    elif choice == "2":
        return "linux"
    else:
        print_error("Invalid selection. Please choose 1 or 2.")
        return select_os()


def select_num_ips():
    """
    Allows the user to select the number of IPs to generate.
    """
    try:
        num_ips = int(input("Enter the number of IPs to generate (1-100): "))
        if 1 <= num_ips <= 100:
            return num_ips
        else:
            print_error("Please enter a number between 1 and 100.")
            return select_num_ips()
    except ValueError:
        print_error("Invalid input. Please enter a valid number.")
        return select_num_ips()


def main():
    try:
        title()
        scan_type = select_scan_type()

        if scan_type == "local":
            print_info("Performing Local Scan on 127.0.0.1...")
            ip_list = ["127.0.0.1"]
        else:
            region = select_region()
            os_type = select_os()
            num_ips = select_num_ips()

            print_info(f"Selected Region: {region.replace('_', ' ').title()}")
            print_info(f"Operating System: {os_type.title()}")
            print_info(f"Generating {num_ips} random IPs for {region.replace('_', ' ').title()}...")

            ip_list = generate_ips(region, num_ips, os_type)

            if not ip_list:
                print_error("No reachable IPs found. Exiting.")
                return

        print_info(f"{len(ip_list)} reachable IP(s) found.")

        print_step("Fetching CVE Data...")
        fetch_cve_data()

        print_step("Scanning Network...")
        for ip in ip_list:
            print_info(f"Scanning IP: {ip}")
            try:
                scan_results = scan_network(ip)
                logger.log_host_info(ip, [result["port"] for result in scan_results])
                time.sleep(0.5)

                print_step("Enumerating Services...")
                for result in scan_results:
                    banner = grab_banner(result["host"], result["port"])
                    print_info(f"Banner for {result['host']}:{result['port']} -> {banner}")
                    logger.log_service_info(result["host"], result["port"], result["service"], result["version"])
                    time.sleep(0.2)

                    print_step("Matching Vulnerabilities...")
                    matches = match_vulnerability(result["service"], result["version"])
                    if matches:
                        for match in matches:
                            print_info(f"---<>---## Vulnerability Found: {match['id']} - {match['description']}")
                            logger.log_vulnerability(result["host"], result["port"], match["id"], match["description"])
                    else:
                        print_info("No Vulnerability Found.")
                        logger.log_no_vulnerabilities(result["host"], result["port"])
            except Exception as e:
                print_error(f"Error scanning IP {ip}: {e}")
    except Exception as e:
        print_error(f"Critical error in the program: {e}")


if __name__ == "__main__":
    main()
