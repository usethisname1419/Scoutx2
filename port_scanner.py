import nmap


def scan_network(target_ip):
    # Define the services and their associated ports to check for
    target_services = {
        "apache": [80, 443],  # HTTP/HTTPS for Apache
        "ssh": [22],  # SSH
        "ftp": [21],  # FTP
        "mysql": [3306],  # MySQL
        "rdp": [3389]  # RDP
    }
    target_ports = []
    for ports in target_services.values():
        target_ports.extend(ports)

    ports_str = ",".join(map(str, target_ports))

    scanner = nmap.PortScanner()
    scanner.scan(hosts=target_ip, arguments=f'-p {ports_str} -sV')
    print(f"[DEBUG] Raw nmap scan results for {target_ip}: {scanner.scaninfo()}")
    print(f"[DEBUG] Detected hosts: {scanner.all_hosts()}")
    result = []

    # Loop through the hosts and protocols to extract relevant service details
    for host in scanner.all_hosts():
        for proto in scanner[host].all_protocols():
            for port in scanner[host][proto]:
                service = scanner[host][proto][port]

                # Check if the service is one of the targeted services
                if service.get("name") in target_services and port in target_services[service.get("name")]:
                    result.append({
                        "host": host,
                        "port": port,
                        "service": service.get("name"),
                        "version": service.get("version")
                    })

    return result
