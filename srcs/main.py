from cgitb import lookup
import string
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
	counter = 0
	li = []
	for i in data:
		if i != '\n':
			string += string.join(i)
		if i == '\n':
			if counter == 0:
				li = list(string.split("\n"))
				counter = 1
				string = ""
			else:
				li.extend(list(string.split("\n")))
				string = ""
	return li

def main(file):
	data = read_data(file)
	li = add_my_dict(data)
	uuid_list = []
	uuid_list_dict = {}
	for i in li:
		string = str(i)
		my_dict = json.loads(string)
		uuid_list.append(my_dict["visitor_uuid"])
	uuid_list_dict = uuid_list[0]
	# if (uuid_list.count(uuid_list_dict)):
	# 	uuid_list_dict[0].add(my_dict["visitor_country"])
	# 	print(uuid_list_dict)
if __name__ == '__main__':
	main(args.file)