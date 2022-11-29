import pandas as pd
import argparse
import json

parser = argparse.ArgumentParser(description="Reading the valid Document")
parser.add_argument('file', type=str, help='reading')
args = parser.parse_args()

def	read_data(file):
	fd = open(file, "r")
	data = fd.read()
	fd.close()
	return data

def	add_my_dict(data):
	string = ""
	for i in data:
		string += string.join(i)
		if i == '\n':
			break
	return string

def main(file):
	data = read_data(file)
	string = add_my_dict(data)
	print(string)
if __name__ == '__main__':
	main(args.file)