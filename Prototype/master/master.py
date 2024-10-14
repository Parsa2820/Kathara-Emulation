import socket
import threading
import time

BROADCAST_PORT = 5000
TCP_PORT = 6000
BROADCAST_MESSAGE = "DISCOVER_PEERS"
BUFFER_SIZE = 1024
BROADCAST_COOLDOWN = 5

def broadcast_message():
    """Function to broadcast a message over UDP."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            s.sendto(BROADCAST_MESSAGE.encode(), ('<broadcast>', BROADCAST_PORT))
            print("Broadcast message sent.")
            time.sleep(BROADCAST_COOLDOWN)

def handle_tcp_connection():
    """Function to handle incoming TCP connections and receive IP addresses from peers."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", TCP_PORT))
        s.listen(5)
        print(f"Listening for TCP connections on port {TCP_PORT}...")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(BUFFER_SIZE)
                print(f"Received peer IP address: {data.decode()} from {addr}")

if __name__ == "__main__":
    # Start broadcasting in a separate thread
    threading.Thread(target=broadcast_message, daemon=True).start()

    # Start handling TCP connections in a separate thread
    threading.Thread(target=handle_tcp_connection, daemon=True).start()

    # Keep the main thread alive for 30 seconds
    time.sleep(30)
