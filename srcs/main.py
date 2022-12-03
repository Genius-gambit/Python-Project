from cgitb import lookup
from csv import reader
import string
import pandas as pd
import argparse
import json
import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# from matplotlib import pyplot as plt
import numpy
import pycountry_convert as pc
# from iso3166 import countries

root = tk.Tk()
# plt.use('TkAgg')
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

def get_visitor_brows(li):
	brows = []
	for i in li:
		string = str(i)
		my_dict = json.loads(string)
		brows.append(my_dict["visitor_useragent"])
	return brows

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

def get_count_conts(li, cont, id):
	count = 0
	length = len(li)
	for i in li:
		string = str(i)
		dict1 = json.loads(string)
		if (dict1["visitor_uuid"] == id):
			if (cont != "Unknown"):
				if (pc.convert_continent_code_to_continent_name(pc.country_alpha2_to_continent_code(dict1["visitor_country"])) == cont):
					count += 1
			else:
				count += 1
	return count

def get_count_brows(li, browser, id):
	count = 0
	length = len(li)
	for i in li:
		string = str(i)
		dict1 = json.loads(string)
		if (dict1["visitor_uuid"] == id):
			if (str.split(dict1["visitor_useragent"], " ")[0] == browser):
				count += 1
	return count

def get_count_sbrows(li, browser, id):
	count = 0
	length = len(li)
	for i in li:
		string = str(i)
		dict1 = json.loads(string)
		if (dict1["visitor_uuid"] == id):
			if (str.split(str.split(dict1["visitor_useragent"], " ")[0], "/")[0] == browser):
				count += 1
	return count

def create_dict_uuid_countries(id, countries, li):
	dict = {}
	dict.update({"uuid" : id})
	length_countries = len(countries)
	for i in range(length_countries):
		country = countries[i]
		count = get_count(li, country, id)
		dict.update({country : count})
	return (dict)

def create_dict_uuid_conts(id, countries, li):
	dict = {}
	dict.update({"uuid" : id})
	length_countries = len(countries)
	for i in range(length_countries):
		country = countries[i]
		if country != 'ZZ':
			cont = pc.convert_continent_code_to_continent_name(pc.country_alpha2_to_continent_code(country))
		else:
			cont = "Unknown"
		count = get_count_conts(li, cont, id)
		dict.update({cont : count})
	return (dict)

def create_dict_uuid_brows(id, browsers, li):
	dict = {}
	dict.update({"uuid" : id})
	length = len(browsers)
	for i in range(length):
		browser = browsers[i]
		count = get_count_brows(li, browser, id)
		dict.update({browser : count})
	return (dict)

def create_dict_uuid_sbrows(id, sbrowsers, li):
	dict = {}
	dict.update({"uuid" : id})
	length = len(sbrowsers)
	for i in range(length):
		browser = sbrowsers[i]
		count = get_count_sbrows(li, browser, id)
		dict.update({browser : count})
	print(dict)
	return (dict)

def get_readers(li):
	readers_list = []
	unique_readers_list = []
	freq_occurences = []
	read_dict = {}
	for i in li:
		string = str(i)
		my_dict = json.loads(string)
		if (my_dict["env_type"] == "reader"):
			readers_list.append(my_dict["visitor_uuid"])
	length = len(readers_list)
	for i in range(length):
		if (readers_list[i] not in unique_readers_list):
			unique_readers_list.append(readers_list[i])
	length = len(unique_readers_list)
	for i in range(len(unique_readers_list)):
		count = 0
		for j in range(len(readers_list)):
			if (unique_readers_list[i] == readers_list[j]):
				count += 1
		freq_occurences.append(count)
	for i in range(len(unique_readers_list)):
		read_dict.update({unique_readers_list[i] : freq_occurences[i]})
	read_dict = dict(sorted(read_dict.items(), key=lambda item: item[1], reverse=True))
	return (read_dict)


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

def filt_brows(browsers):
	length = len(browsers)
	for i in range(length):
		browsers[i] = str.split(browsers[i], " ")[0]
	return (browsers)

def sp_browsers(browsers):
	sbrowsers = []
	length = len(browsers)
	for i in range(length):
		sbrowsers.append(str.split(browsers[i], "/")[0])
	return (sbrowsers)


e = tk.Entry(root, width=50, bg="white")
e.pack(pady=10)
file = args.file
uuid = ""
data = read_data(file)
li = add_my_dict(data)
uuid_list = get_visitor_uuids(li)
countries = get_visitor_countries(li)
browsers = get_visitor_brows(li)
browsers = filt_brows(browsers)
sbrowsers = sp_browsers(browsers)
readers = get_readers(li)
unique_countries = get_unique_countries(li)

def plt_hist(list_dict_identifiers, list_dict_vals, title, x_label, y_label):
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.xticks(None, None, ha='right', rotation=55, fontsize=5)
	plt.bar(list_dict_identifiers, list_dict_vals, width=0.4)
	plt.ylim(0, max(list_dict_vals) + 1)
	plt.show()

def get_hist_countries():
	global uuid
	uuid = e.get()
	if uuid in uuid_list:
		uuid_dict = create_dict_uuid_countries(uuid, countries, li)
		uuid_dict.pop("uuid")
		list_dict_identifiers = list(uuid_dict.keys())
		for i in range(len(list_dict_identifiers)):
			if (list_dict_identifiers[i] != "ZZ"):
				list_dict_identifiers[i] = pc.country_alpha2_to_country_name(list_dict_identifiers[i])
			else:
				list_dict_identifiers[i] = "Unknown"
		list_dict_vals = list(uuid_dict.values())
		plt_hist(list_dict_identifiers, list_dict_vals, "Total Views", "Countries", "Frequency")
	else:
		messagebox.showerror("Error!", "Invalid UUID")

def get_hist_continents():
	global uuid
	uuid = e.get()
	if uuid in uuid_list:
		uuid_dict = create_dict_uuid_conts(uuid, countries, li)
		uuid_dict.pop("uuid")
		list_dict_identifiers = list(uuid_dict.keys())
		list_dict_vals = list(uuid_dict.values())
		plt_hist(list_dict_identifiers, list_dict_vals, "Total Views", "Continents", "Frequency")
	else:
		messagebox.showerror("Error!", "Invalid UUID")

def get_hist_browser():
	global uuid
	uuid = e.get()
	if uuid in uuid_list:
		uuid_dict = create_dict_uuid_brows(uuid, browsers, li)
		print(uuid_dict)
		uuid_dict.pop("uuid")
		list_dict_identifiers = list(uuid_dict.keys())
		list_dict_vals = list(uuid_dict.values())
		plt_hist(list_dict_identifiers, list_dict_vals, "Total Views", "Browsers", "Frequency")
	else:
		messagebox.showerror("Error!", "Invalid UUID")

def get_hist_sbrowser():
	global uuid
	uuid = e.get()
	if uuid in uuid_list:
		uuid_dict = create_dict_uuid_sbrows(uuid, sbrowsers, li)
		uuid_dict.pop("uuid")
		list_dict_identifiers = list(uuid_dict.keys())
		print(list_dict_identifiers)
		list_dict_vals = list(uuid_dict.values())
		plt_hist(list_dict_identifiers, list_dict_vals, "Total Views", "Browsers", "Frequency")
	else:
		messagebox.showerror("Error!", "Invalid UUID")

def top_readers():
	reader_keys = readers.keys()
	reader_vals = readers.values()
	iterate = 0
	raw_keys = []
	raw_vals = []
	for i in reader_keys:
		if (iterate == 10):
			break
		raw_keys.append(i)
		iterate += 1
	iterate = 0
	for i in reader_vals:
		if (iterate == 10):
			break
		raw_vals.append(i)
		iterate += 1
	plt_hist(raw_keys, raw_vals, "Top 10 Readers", "UUID", "Frequecies")

def main():
	root.title("Enter a valid UUID")
	Button_1 = tk.Button(root, text="Get Histogram for views in countries", command=get_hist_countries)
	Button_1.pack()
	Button_2 = tk.Button(root, text="Get Histogram for views in continents", command=get_hist_continents)
	Button_2.pack()
	Button_3 = tk.Button(root, text="Get Histogram for browser", command=get_hist_browser)
	Button_3.pack()
	Button_4 = tk.Button(root, text="Get Histogram for Specific browser", command=get_hist_sbrowser)
	Button_4.pack()
	Button_4 = tk.Button(root, text="Get Top 10 Readers", command=top_readers)
	Button_4.pack()
	root.mainloop()

if __name__ == '__main__':
	main()