from cgitb import lookup
import string
import pandas as pd
import argparse
import json
import tkinter

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

def get_visitor_uuids(li):
	uuid_list = []
	for i in li:
		string = str(i)
		my_dict = json.loads(string)
		uuid_list.append(my_dict["visitor_uuid"])
	length = len(uuid_list)
	uuid_list_unique = []
	for i in range(length):
		if (uuid_list[i] not in uuid_list_unique):
			uuid_list_unique.append(uuid_list[i])
	return uuid_list_unique

def get_visitor_countries(li):
	countries = []
	for i in li:
		string = str(i)
		my_dict = json.loads(string)
		countries.append(my_dict["visitor_country"])
	return countries

def get_count(li, country, id):
	count = 0
	length = len(li)
	for i in li:
		string = str(i)
		dict1 = json.loads(string)
		if (dict1["visitor_uuid"] == id):
			if (dict1["visitor_country"] == country):
				count += 1
	return count

def create_dict_uuid(id, countries, li):
	dict = {}
	dict.update({"uuid" : id})
	length_countries = len(countries)
	for i in range(length_countries):
		country = countries[i]
		count = get_count(li, country, id)
		dict.update({country : count})
	return (dict)

def main(file):
	data = read_data(file)
	li = add_my_dict(data)
	uuid_list = get_visitor_uuids(li)
	countries = get_visitor_countries(li)
	# country = str(countries[0])
	length = len(uuid_list)
	list_dict_identifiers = []
	list_dict_vals = []
	for i in range(length):
		id = str(uuid_list[i])
		uuid_dict = create_dict_uuid(id, countries, li)
		list_dict_identifiers.append(list(uuid_dict))
		list_dict_vals.append(list(uuid_dict.values()))
		if (i == 4):
			break
	# print(list_dict_identifiers[5])
	# print(list_dict_vals[5])

if __name__ == '__main__':
	main(args.file)