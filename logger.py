import logging
from colorama import Fore, Style, init
def print_info(message):
    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} {message}")


def print_step(step_message):
    print(f"{Fore.BLUE}[STEP]{Style.RESET_ALL} {step_message}")


def print_error(error_message):
    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {error_message}")


def configure_logging(log_file="scan_log.txt"):
    """
    Configures the logging settings to log vulnerabilities, hosts, ports, and services.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.info("Log Initialized: Vulnerability Scanner")

def log_host_info(host, open_ports):
    """
    Logs information about the scanned host and its open ports.
    """
    message = f"Host: {host} - Open Ports: {', '.join(str(port) for port in open_ports)}"
    logging.info(message)

def log_service_info(host, port, service, version=None):
    """
    Logs details about a service running on a specific host and port.
    """
    version_info = f" (Version: {version})" if version else ""
    message = f"Service Found - Host: {host}, Port: {port}, Service: {service}{version_info}"
    logging.info(message)

def log_vulnerability(host, port, vuln_id, description):
    """
    Logs details about a vulnerability found for a specific host and port.
    """
    message = (
        f"Vulnerability Found - Host: {host}, Port: {port}, "
        f"Vulnerability ID: {vuln_id}, Description: {description}"
    )
    logging.info(message)

def log_no_vulnerabilities(host, port):
    """
    Logs when no vulnerabilities are found for a specific host and port.
    """
    message = f"No Vulnerabilities Found - Host: {host}, Port: {port}"
    logging.info(message)
