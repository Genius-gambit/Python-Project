from cgitb import lookup
import string
import uuid
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
	uuid_country = []
	for i in li:
		string = str(i)
		my_dict = json.loads(string)
		uuid_list.append(my_dict["visitor_uuid"])
		uuid_country.append(my_dict["visitor_country"])
	uuid_list_dict["visitor_uuid"] = uuid_list[0]
	uuid_list_dict.update({uuid_country[0] : 1})
	if (uuid_list[1] == uuid_list_dict.get("visitor_uuid")):
		if (uuid_list_dict.get(uuid_list[1]) == None):
			print(uuid_list_dict.get(uuid_list[1]))
	# print(uuid_list_dict.get("visitor_uuid"))
	# print(uuid_list_dict)
if __name__ == '__main__':
	main(args.file)