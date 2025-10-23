import os
import sys

import concurrent.futures
import asyncio
import socket

workerCount = 3

def ProcessRoutine(fd: int, index: int):
	
	async def server_routine(df: int, index: int):
		sock = socket.fromfd(fd, socket.AF_UNIX, socket.SOCK_STREAM)

		async def server_runner(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
			print(f"child process {index} incoming client")
			try:
				while not reader.at_eof():
					data = await reader.readline()
					data_received = data.decode()
					print(f"child process {index} receved: {data_received}")
					if data_received == "EOF\n":
						print(f"child process {index} received EOF signal, ending transmission")
						asyncio.create_task(server.close())   # Not working! need to find another way to stop the server
						break
					writer.write(b"sending ack: " + data)
					await writer.drain()
			except ConnectionResetError as e:
				print(f"child process {index} connection reset: {e}")
			print(f"child process end transmission with server process {index}")

		server = await asyncio.start_unix_server(server_runner, sock=sock)
		print("server started :", index)
		async with server:
			await server.serve_forever()

	asyncio.run(server_routine(fd, index))
	print(f"child process {index} done")
	return 0
	


if __name__ == "__main__":
	socket_path = '/tmp/unixSocketTest.sock'

	# Create a Unix socket
	if os.path.exists(socket_path):
		os.remove(socket_path)
	server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind(socket_path)
	server.listen()

	print(f"server listening on {socket_path}")

	with concurrent.futures.ProcessPoolExecutor(max_workers=workerCount) as executor:
		submit_list = []
		for i in range(workerCount):
			fd = server.fileno()
			print("submitting process with fd:", fd)
			future = executor.submit(ProcessRoutine, fd, i)
			submit_list.append(future)

		print("all processes submitted")

		for future in concurrent.futures.as_completed(submit_list):
			try:
				result = future.result()
			except Exception as exc:
				print(f'generated an exception: {exc}')
			else:
				print(f'process completed with result: {result}')
	print("all processes done")