import socket
def grab_banner(ip, port):
    """
    Grabs the banner from a service running on the specified IP and port.
    Handles different protocols (HTTP, FTP, SSH, etc.).
    """
    try:
        with socket.create_connection((ip, port), timeout=10) as conn:
            if port == 80 or port == 443:  # HTTP/HTTPS
                conn.send(b"HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n")
            elif port == 21:  # FTP
                conn.send(b"USER anonymous\r\n")
            elif port == 22:  # SSH
                conn.send(b"\r\n")
            else:  # Default for unknown services
                conn.send(b"HEAD / HTTP/1.1\r\n\r\n")

            return conn.recv(1024).decode().strip()
    except Exception as e:
        return f"Error: {e}"
