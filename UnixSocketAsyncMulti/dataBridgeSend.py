import os
import sys

import socket

sock_path = '/tmp/suricata_output.sock'
client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

client_socket.connect(sock_path)
print(f"Connected to {sock_path}")

client_socket.sendall(b"hello world!")
print("Sended message")

client_socket.close()
print("closed client")


