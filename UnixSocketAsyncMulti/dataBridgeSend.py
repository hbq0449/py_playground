import os
import sys

import socket

sock_path = '/tmp/unixSocketTest.sock'
with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client_socket:

	client_socket.connect(sock_path)
	print(f"Connected to {sock_path}")

	client_socket.sendall(b"hello world!\n")
	print("Sended message")
	data = client_socket.recv(1024)
	print(f"Received: {data.decode()}")

	client_socket.sendall(b"another line message\n")
	print("Sended another message")
	data = client_socket.recv(1024)
	print(f"Received: {data.decode()}")

	client_socket.sendall(b"EOF\n")

	client_socket.shutdown(socket.SHUT_WR)
	


