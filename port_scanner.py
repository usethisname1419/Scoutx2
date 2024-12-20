import nmap
from logger import print_info
def scan_network(target_ip):
    # Define the services and their associated ports to check for
    target_services = {
        "apache": [80, 443, 8080],  # HTTP/HTTPS for Apache or Tomcat
        "ssh": [22],  # SSH
        "ftp": [21],  # FTP
        "mysql": [3306],  # MySQL
        "rdp": [3389],  # RDP
        "netbios": [137, 138, 139],  # NetBIOS
        "smb": [445],  # SMB
        "dns": [53],  # DNS
        "http-proxy": [3128, 8080],  # Common proxy ports
        "postgresql": [5432],  # PostgreSQL
        "redis": [6379],  # Redis
        "elasticsearch": [9200, 9300],  # Elasticsearch
        "mongodb": [27017, 27018],  # MongoDB
        "rabbitmq": [5672],  # RabbitMQ
    }

    unique_ports = sorted(set(port for ports in target_services.values() for port in ports))
    ports_str = ",".join(map(str, unique_ports))

    scanner = nmap.PortScanner()
    scanner.scan(hosts=target_ip, arguments=f'-sV -p {ports_str}')
    result = []

    for host in scanner.all_hosts():
        print_info("")
        print("======================")
        print("")
        print(f"\n  Host: {host}")
        print(f"  State: {scanner[host].state()}")

        for proto in scanner[host].all_protocols():
            print(f"\n    Protocol: {proto}")

            for port in sorted(scanner[host][proto].keys()):
                service = scanner[host][proto][port]
                print(f"      Port: {port}")
                print(f"        State: {service.get('state', 'unknown')}")
                print(f"        Service: {service.get('name', 'unknown')}")
                print(f"        Version: {service.get('version', 'unknown')}")
                print("")

                # Check if the service is one of the targeted services
                if service.get("name") in target_services and port in target_services[service.get("name")]:
                    result.append({
                        "host": host,
                        "port": port,
                        "service": service.get("name"),
                        "version": service.get("version")
                    })

    return result
