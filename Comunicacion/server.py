# echo-server.py

import socket

HOST = "169.254.164.71"  # Standard loopback interface address (localhost)
PORT = 90  # Port to listen on (non-privileged ports are > 1023)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = str(300).encode('utf8')
            conn.sendall(data)
            break