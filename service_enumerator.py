import socket
from logger import print_error
def grab_banner(ip, port):
    """
    Grabs the banner from a service running on the specified IP and port.
    Supports a wide range of common services.
    """
    try:
        with socket.create_connection((ip, port), timeout=10) as conn:
            # Send protocol-specific requests for target services
            if port in [80, 443, 8080, 8000, 8888]:  # HTTP/HTTPS
                conn.sendall(b"HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n")
            elif port == 21:  # FTP
                conn.sendall(b"USER anonymous\r\n")
            elif port == 22:  # SSH
                conn.sendall(b"SSH-2.0-Scoutx2\r\n")
            elif port == 3306:  # MySQL
                conn.sendall(b"\x00\x00\x00\x00")
            elif port == 3389:  # RDP
                conn.sendall(b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x12\x34\x00\x02\x00\x00\x00\x00")
            elif port in [137, 138, 139]:  # NetBIOS
                conn.sendall(b"\x81\x00\x00\x01\x00\x00\x00\x00\x00\x00\x20\x43\x4b")
            elif port == 445:  # SMB
                conn.sendall(b"\x00")
            elif port == 53:  # DNS
                conn.sendall(b"\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x04test\x03com\x00\x00\x01\x00\x01")
            elif port in [9200, 9300]:  # Elasticsearch
                conn.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
            elif port == 5432:  # PostgreSQL
                conn.sendall(b"\x00\x00\x00\x08\x04\xd2\x16\x2f")
            elif port == 6379:  # Redis
                conn.sendall(b"PING\r\n")
            elif port == 27017:  # MongoDB
                conn.sendall(b"\x3a\x00\x00\x00\x0a\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00admin\x00")
            elif port == 5672:  # RabbitMQ
                conn.sendall(b"AMQP\r\n")
            elif port in [3128, 8080]:  # HTTP Proxy
                conn.sendall(b"CONNECT example.com:80 HTTP/1.1\r\nHost: example.com\r\n\r\n")
            else:  # Handle unexpected ports
                return f"[DEBUG] No specific protocol handler for port {port}."

            # Receive banner and handle response
            banner = conn.recv(2048).decode(errors="ignore").strip()
            return banner if banner else f"[DEBUG] No banner received on port {port}."
    except socket.timeout:
        print_error(f"Timeout: Unable to connect to {ip}:{port}.")
    except ConnectionRefusedError:
        print_error(f"Connection Refused: {ip}:{port}.")
    except Exception as e:
        print_error(f"Error: {e}")
