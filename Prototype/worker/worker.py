import socket
import threading
import time

BROADCAST_PORT = 5000
TCP_PORT = 6000
BROADCAST_MESSAGE = "DISCOVER_PEERS"
BUFFER_SIZE = 1024

def listen_for_broadcast():
    """Function to listen for broadcast messages from master."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("", BROADCAST_PORT))
        print(f"Listening for broadcasts on port {BROADCAST_PORT}...")
        while True:
            data, addr = s.recvfrom(BUFFER_SIZE)
            if data.decode() == BROADCAST_MESSAGE:
                print(f"Discovered master at {addr}")
                connect_to_master(addr[0])

def connect_to_master(peer_ip):
    """Function to connect to a peer using TCP and send this node's IP address."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((peer_ip, TCP_PORT))
            my_ip = s.getsockname()[0]
            s.send(my_ip.encode())
            print(f"Sent my IP ({my_ip}) to peer at {peer_ip}.")
        except Exception as e:
            print(f"Failed to connect to peer at {peer_ip}: {e}")

if __name__ == "__main__":
    # Start listening for broadcast messages in a separate thread
    threading.Thread(target=listen_for_broadcast, daemon=True).start()

    # Keep the main thread alive for 30 seconds
    time.sleep(30)