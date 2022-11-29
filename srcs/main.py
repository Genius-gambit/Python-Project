import pandas as pd
import argparse
import json

parser = argparse.ArgumentParser(description="Reading the valid Document")
parser.add_argument('file', type=str, help='reading')
args = parser.parse_args()

def	read_data(file):
	fd = open(file)
	data = json.load(fd)
	for i in data["details"]:
		print(i)
	fd.close()

def main(file):
	read_data(file)
if __name__ == '__main__':
	main(args.file)