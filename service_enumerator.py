import socket

def grab_banner(ip, port):
    """
    Grabs the banner from a service running on the specified IP and port.
    Focused on apache, ssh, ftp, mysql, and rdp.
    """
    try:
        with socket.create_connection((ip, port), timeout=10) as conn:
            # Send protocol-specific requests for target services
            if port == 80 or port == 443:  # Apache (HTTP/HTTPS)
                conn.sendall(b"HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n")
            elif port == 21:  # FTP
                conn.sendall(b"USER anonymous\r\n")
            elif port == 22:  # SSH
                conn.sendall(b"\r\n")
            elif port == 3306:  # MySQL
                conn.sendall(b"\x00\x00\x00\x00")  # MySQL handshake
            elif port == 3389:  # RDP
                conn.sendall(b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x12\x34\x00\x02\x00\x00\x00\x00")  # RDP client hello
            else:  # Handle unexpected ports
                return f"No specific protocol handler for port {port}."
            
            # Receive banner and handle response
            banner = conn.recv(2048).decode(errors="ignore").strip()
            return banner if banner else f"No banner received on port {port}."
    except socket.timeout:
        return f"Timeout: Unable to connect to {ip}:{port}."
    except ConnectionRefusedError:
        return f"Connection Refused: {ip}:{port}."
    except Exception as e:
        return f"Error: {e}"
