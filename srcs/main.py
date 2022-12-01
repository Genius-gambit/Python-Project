from cgitb import lookup
import string
import pandas as pd
import argparse
import json
import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot as plt
import numpy

root = tk.Tk()
root.geometry("750x250")

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

def	get_unique_countries(li):
	countries = []
	for i in li:
		string = str(i)
		my_dict = json.loads(string)
		countries.append(my_dict["visitor_country"])
	length = len(countries)
	u_countries = []
	for i in range(length):
		if (countries[i] not in u_countries):
			u_countries.append(countries[i])
	return u_countries

e = tk.Entry(root, width=50, bg="white")
e.pack(pady=10)
file = args.file
uuid = ""
data = read_data(file)
li = add_my_dict(data)
uuid_list = get_visitor_uuids(li)
countries = get_visitor_countries(li)
unique_countries = get_unique_countries(li)

def get_hist_countries():
	global uuid
	uuid = e.get()
	if uuid in uuid_list:
		uuid_dict = create_dict_uuid(uuid, countries, li)
		uuid_dict.pop("uuid")
		list_dict_identifiers = list(uuid_dict.keys())
		list_dict_vals = list(uuid_dict.values())
		plt.title("Number of Times Viewed")
		plt.xlabel("Countries")
		plt.ylabel("Frequency")
		plt.bar(unique_countries, list_dict_vals, width=0.4)
		plt.ylim(0, max(list_dict_vals) + 1)
		plt.show()
	else:
		messagebox.showerror("Error!", "Invalid UUID")

def main():
	root.title("Enter a valid UUID")
	Button_1 = tk.Button(root, text="Go", command=get_hist_countries)
	Button_1.pack()
	root.mainloop()

if __name__ == '__main__':
	main()