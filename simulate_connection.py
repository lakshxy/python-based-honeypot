import socket

HOST = 'localhost'  # The server's hostname or IP address
PORT = 9999         # The port used by the honeypot server

# Create a socket connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Connect to the honeypot
    s.sendall(b'Hello, honeypot!')  # Send a message
    data = s.recv(1024)  # Receive a response

print('Received', repr(data))  # Print the response