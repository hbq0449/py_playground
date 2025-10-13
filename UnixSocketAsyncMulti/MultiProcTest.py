import os
import sys

import concurrent.futures
import time


def runner(counter):
	print(f"running {counter}")
	time.sleep(2)
	print(f'after sleep {counter}')
	return counter

if __name__ == "__main__":
	with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
		submit_list = []
		for i in range(10):
			print("submit count:", i)
			future = executor.submit(runner, i)
			submit_list.append(future)
		
		print("all submitted")

		for future in concurrent.futures.as_completed(submit_list):
			try:
				result = future.result()
			except Exception as exc:
				print(f'generated an exception: {exc}')
			else:
				print(f'result: {result}')
	print("all done")


		