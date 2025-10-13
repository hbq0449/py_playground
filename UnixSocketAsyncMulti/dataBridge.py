import os
import sys

import asyncio

async def main():
	socket_path = '/tmp/suricata_output.sock'
	async def handle_client(reader, writer):
		print("incoming client")
		while not reader.at_eof():
			data = await reader.readline()
			print(f"server receved: {data.decode()}")

	server = await asyncio.start_unix_server(handle_client, path=socket_path)
	print(f"server listen on {socket_path}")

	await server.serve_forever()

if __name__ == "__main__":
	asyncio.run(main())