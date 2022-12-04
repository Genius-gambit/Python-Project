from ast import arg
from cgitb import lookup
from csv import reader
from operator import length_hint
from pydoc import doc
import string
from tabnanny import check
import pandas as pd
import argparse
import json
import tkinter as tk
from tkinter import messagebox
import matplotlib
from traitlets import default
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# from matplotlib import pyplot as plt
import numpy
import pycountry_convert as pc
# from iso3166 import countries

# plt.use('TkAgg')
parser = argparse.ArgumentParser(description="Reading the valid Document")
parser.add_argument('-u', dest = 'user_uuid',
                    action = 'store', help = 'user_uuid')
parser.add_argument('-d', dest = 'doc_uuid',
                    action = 'store', help = 'doc_uuid')
parser.add_argument('-t', dest = 'task_id',
                    action = 'store', help = 'task_id')
parser.add_argument('-f', dest = 'file',
                    action = 'store', help = 'filename', required=True)
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
		if (dict1.get("subject_doc_id") == id):
			if (dict1["visitor_country"] == country):
				count += 1
	return count

def get_count_conts(li, cont, id):
	count = 0
	length = len(li)
	for i in li:
		string = str(i)
		dict1 = json.loads(string)
		if (dict1.get("subject_doc_id") == id):
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

def get_docs(li):
	docs = []

	for i in li:
		string = str(i)
		my_dict = json.loads(string)
		if (my_dict.get("subject_type") != None):
			docs.append(my_dict.get("subject_doc_id"))
	return docs

def get_unique_docs(li, document_list):
	length = len(document_list)
	u_docs = []
	for i in range(length):
		if (document_list[i] not in u_docs):
			u_docs.append(document_list[i])
	return u_docs

if (args.user_uuid == None):
		if (args.doc_uuid == None):
			if (args.task_id == None):
				root = tk.Tk()
				root.geometry("750x350")
				e = tk.Entry(root, width=50, bg="white")
				e.pack(pady=10)
				e.insert(0, "Document UUID: ")
				f = tk.Entry(root, width=50, bg="white")
				f.insert(0, "Visitor UUID: ")
				f.pack(pady=10)
elif (args.task_id == "7"):
	root = tk.Tk()
	root.geometry("750x350")
	e = tk.Entry(root, width=50, bg="white")
	e.pack(pady=10)
	e.insert(0, "Document UUID: ")
	f = tk.Entry(root, width=50, bg="white")
	f.insert(0, "Visitor UUID: ")
	f.pack(pady=10)
file = args.file
uuid = ""
data = read_data(file)
li = add_my_dict(data)
uuid_list = get_visitor_uuids(li)
document_list = get_docs(li)
u_docs = get_unique_docs(li, document_list)
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
	e.delete(0, len("Document UUID: "))
	uuid = e.get()
	e.insert(0, "Document UUID: ")
	if uuid in u_docs:
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
	e.delete(0, len("Document UUID: "))
	uuid = e.get()
	e.insert(0, "Document UUID: ")
	if uuid in u_docs:
		uuid_dict = create_dict_uuid_conts(uuid, countries, li)
		uuid_dict.pop("uuid")
		list_dict_identifiers = list(uuid_dict.keys())
		list_dict_vals = list(uuid_dict.values())
		plt_hist(list_dict_identifiers, list_dict_vals, "Total Views", "Continents", "Frequency")
	else:
		messagebox.showerror("Error!", "Invalid UUID")


def get_hist_browser():
	global uuid
	f.delete(0, len("Visitor UUID: "))
	uuid = f.get()
	f.insert(0, "Visitor UUID: ")
	if uuid in uuid_list:
		uuid_dict = create_dict_uuid_brows(uuid, browsers, li)
		uuid_dict.pop("uuid")
		list_dict_identifiers = list(uuid_dict.keys())
		list_dict_vals = list(uuid_dict.values())
		plt_hist(list_dict_identifiers, list_dict_vals, "Total Views", "Browsers", "Frequency")
	else:
		messagebox.showerror("Error!", "Invalid UUID")

def get_hist_sbrowser():
	global uuid
	f.delete(0, len("Visitor UUID: "))
	uuid = f.get()
	f.insert(0, "Visitor UUID: ")
	if uuid in uuid_list:
		uuid_dict = create_dict_uuid_sbrows(uuid, sbrowsers, li)
		uuid_dict.pop("uuid")
		list_dict_identifiers = list(uuid_dict.keys())
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

def get_uuid_readers():
	visitor_uuids = []
	global uuid
	uuid = e.get()
	if (uuid in u_docs):
		for i in li:
			string = str(i)
			my_dict = json.loads(string)
			if (my_dict.get("subject_doc_id") != None):
				if (my_dict.get("subject_doc_id") == uuid):
					if (my_dict.get("visitor_uuid") not in visitor_uuids):
						visitor_uuids.append(my_dict.get("visitor_uuid"))
	return visitor_uuids

def	execute_countries():
	global uuid
	uuid = args.doc_uuid
	if uuid in u_docs:
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
		print("Error")

def	execute_conts():
	global uuid
	uuid = args.doc_uuid
	if uuid in u_docs:
		uuid_dict = create_dict_uuid_conts(uuid, countries, li)
		uuid_dict.pop("uuid")
		list_dict_identifiers = list(uuid_dict.keys())
		list_dict_vals = list(uuid_dict.values())
		plt_hist(list_dict_identifiers, list_dict_vals, "Total Views", "Continents", "Frequency")
	else:
		print("Error")

def execute_brows():
	global uuid
	uuid = args.user_uuid
	if uuid in uuid_list:
		uuid_dict = create_dict_uuid_brows(uuid, browsers, li)
		uuid_dict.pop("uuid")
		list_dict_identifiers = list(uuid_dict.keys())
		list_dict_vals = list(uuid_dict.values())
		plt_hist(list_dict_identifiers, list_dict_vals, "Total Views", "Browsers", "Frequency")
	else:
		print("Error")

def execute_s_brows():
	global uuid
	uuid = args.user_uuid
	if uuid in uuid_list:
		uuid_dict = create_dict_uuid_sbrows(uuid, sbrowsers, li)
		uuid_dict.pop("uuid")
		list_dict_identifiers = list(uuid_dict.keys())
		list_dict_vals = list(uuid_dict.values())
		plt_hist(list_dict_identifiers, list_dict_vals, "Total Views", "Browsers", "Frequency")
	else:
		print("Error")

def execute():
	if (args.task_id == "2a"):
		execute_countries()
	elif (args.task_id == "2b"):
		execute_conts()
	elif (args.task_id == "3a"):
		execute_brows()
	elif (args.task_id == "3b"):
		execute_s_brows()
	elif (args.task_id == "4"):
		top_readers()

def get_doc_read(uuid):
	doc_uuids = []
	if (uuid in uuid_list):
		for i in li:
			string = str(i)
			my_dict = json.loads(string)
			if (my_dict.get("visitor_uuid") != None):
				if (my_dict.get("visitor_uuid") == uuid):
					if (my_dict.get('subject_doc_id') != None):
						if (my_dict.get('subject_doc_id') not in doc_uuids):
							if (my_dict.get("event_type")) != None:
								if (my_dict.get("event_type")) == "read":
									doc_uuids.append(my_dict.get("subject_doc_id"))
		return doc_uuids

def top_10_doc():
	doc_uuids = {}
	lis_doc = []
	lis_vis = []
	global doc_uuid
	global vis_uuid
	e.delete(0, len("Document UUID: "))
	doc_uuid = e.get()
	e.insert(0, "Document UUID: ")
	f.delete(0, len("Visitor UUID: "))
	vis_uuid = f.get()
	f.insert(0, "Visitor UUID: ")
	if (doc_uuid in u_docs):
		if (vis_uuid in uuid_list):
			sorted_dict = {}
			for j in range(len(u_docs)):
				lis_vis = []
				for i in li:
					string = str(i)
					my_dict = json.loads(string)
					if (my_dict.get("subject_doc_id") != None):
						if (my_dict.get("subject_doc_id") == u_docs[j]):
							if (my_dict.get("visitor_uuid") not in lis_vis):
								lis_vis.append(my_dict.get("visitor_uuid"))
				doc_uuids.update({u_docs[j] : lis_vis})
			count = 0
			for k in sorted(doc_uuids, key=lambda k: len(doc_uuids[k]), reverse=True):
				sorted_dict.update({k : doc_uuids.get(k)})
				count += 1
				print(k)
				if (count == 10):
					break
		else:
			messagebox.showerror("Error!", "Invalid UUID")
	else:
		messagebox.showerror("Error!", "Invalid UUID")

def also_like():
	doc_uuids = {}
	lis_doc = []
	lis_vis = []
	global doc_uuid
	global vis_uuid
	e.delete(0, len("Document UUID: "))
	doc_uuid = e.get()
	e.insert(0, "Document UUID: ")
	f.delete(0, len("Visitor UUID: "))
	vis_uuid = f.get()
	f.insert(0, "Visitor UUID: ")
	sorted_dict = {}
	for j in range(len(u_docs)):
		lis_vis = []
		for i in li:
			string = str(i)
			my_dict = json.loads(string)
			if (my_dict.get("subject_doc_id") != None):
				if (my_dict.get("subject_doc_id") == u_docs[j]):
					if (my_dict.get("visitor_uuid") not in lis_vis):
						lis_vis.append(my_dict.get("visitor_uuid"))
		doc_uuids.update({u_docs[j] : lis_vis})
	count = 0
	for k in sorted(doc_uuids, key=lambda k: len(doc_uuids[k]), reverse=True):
		sorted_dict.update({k : doc_uuids.get(k)})
	readers_trial = sorted_dict.get(doc_uuid)
	readers_docs = []
	final_readers = []
	dict_also_like = {}
	for i in range(len(readers_trial)):
		readers_docs = get_doc_read(str(readers_trial[i]))
		if (len(readers_docs) > 0):
			final_readers.append(readers_docs)
			for j in range(len(final_readers)):
				dict_also_like.update({str(readers_trial[i]) : final_readers[j]})
	length = len(dict_also_like)
	list_readers = list(dict_also_like.keys())
	list_docs = list(dict_also_like.values())
	count = 0
	with open('graph.dot','w') as out:
		for line in ('digraph G {','size="16,16";','splines=true;'):
			out.write('{}\n'.format(line))
		for start in range(len(list_readers)):
			out.write("\"")
			string = list_readers[start]
			out.write(string[len(string) - 4 : len(string)])
			out.write("\"")
			out.write(' -> ')
			out.write("\"")
			string = list_docs[start]
			count = 0
			if (len(string) > 0):
				for j in range(len(string)):
					if (count > 0):
						out.write("\"")
						string1 = list_readers[start]
						out.write(string1[len(string1) - 4 : len(string1)])
						out.write("\"")
						out.write(' -> ')
						out.write("\"")
					string = list_docs[start][j]
					out.write(string[len(string) - 4 : len(string)])
					out.write("\"\n")
					count += 1
		out.write('}\n')

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
	Button_5 = tk.Button(root, text="Get Top 10 Readers", command=top_readers)
	Button_5.pack()
	Button_6 = tk.Button(root, text="Get Readers of UUID", command=top_10_doc)
	Button_6.pack()
	Button_7 = tk.Button(root, text="Graph for Also Like", command=also_like)
	Button_7.pack()
	root.mainloop()

if __name__ == '__main__':
	if (args.task_id == "7"):
		main()
	if (args.user_uuid != None):
		if (args.doc_uuid != None):
			if (args.task_id != None):
				execute()
	else:
		main()