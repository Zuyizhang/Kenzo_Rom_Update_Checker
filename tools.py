#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import *
from bs4 import BeautifulSoup
import os, json, random
import rom_list

def ua_open(urll):
	# Use browser proxy to parse web pages
	# Randomly select the browser UA
	random_number = random.randint(1,4)
	if random_number == 1:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
	elif random_number == 2:
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
	elif random_number == 3:
		headers = {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}
	elif random_number == 4:
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
	req = Request(url = urll, headers = headers)
	try:
		with urlopen(req) as xmldata:
			return xmldata.read()
	except:
		return False

def de_open(urll):
	# The general method of parsing the page
	try:
		with urlopen(urll) as xmldata:
			return xmldata.read()
	except:
		return False

def get_bs(urll):
	# Get beautifulSoup for the source of the page
	if not urll:
		return False
	try:
		# The best use of the default:lxml
		return BeautifulSoup(urll, "lxml")
		# Or use html5lib	
		#~ return BeautifulSoup(urll,"html5lib")
	except:
		return False

def open_failed(name):
	print("\n%s:"%get_rom_name(name))
	print("\n*** Access failed or request timeout!")
	return None

def analyze_failed(name):
	print("\n%s:"%get_rom_name(name))
	print("\n*** Parsing failed! Please tell the author to fix this error!")
	return None

def os_clear_screen(ostype):
	if ostype == "Windows":
		os.system("cls")
	else:
		os.system("clear")

def get_md5_from_file(urll):
	# Download MD5 verification file, 
	# read & return MD5 value and delete verification file.
	try:
		urlretrieve(urll,"tempfile")
	except:
		return "Failed to get!"
	else:
		try:
			with open("tempfile") as md5file:
				fmd5 = md5file.read()
			os.remove("tempfile")
			return fmd5.split(" ")[0]
		except:
			return "Failed to get!"

def get_rom_name(name):
	# Get the item's name by the function name
	roms = rom_list.Rom_List()
	for lists in \
	[roms.rom8_list, roms.rom7_list, roms.rom6_list, roms.other_list]:
		for key,value in lists.items():
			if key == name:
				return value
	return "Unknown item"

def out_put(fast_flag, name, fversion, build_info):
	# Output check results
	print_info = []
	while len(print_info) <= 11:
		print_info.append(None)
	print_info[0] = "\n%s:"%get_rom_name(name)
	print_info[1] = "\n=== The latest version:\n\n    " + fversion
	for key, value in build_info.items():
		if key == "build_type":
			print_info[2] = "\n=== Build type:\n\n    " + value
		elif key == "build_version":
			print_info[3] = "\n=== Build version:\n\n    " + value
		elif key == "fdate":
			print_info[4] = "\n=== Updated:\n\n    " + value
		elif key == "update_log":
			print_info[5] = "\n=== Changelog:\n\n    " + value
		elif key == "fmd5":
			print_info[6] = "\n=== MD5:\n\n    " + value
		elif key == "fsha256":
			print_info[7] = "\n=== sha256:\n\n    " + value
		elif key == "fsha1":
			print_info[8] = "\n=== sha1:\n\n    " + value
		elif key == "flink":
			print_info[9] = "\n=== Download link:\n\n    " + value
		elif key == "fsize":
			print_info[10] = "\n=== Size:\n\n    " + value
	for info in print_info:
		if info == None:
			continue
		print(info)
	saved = None
	if fast_flag == False:
		saved = read_from_json("save.json")
	return saved_update(get_rom_name(name), fversion, saved)

def check_for_update(checked, temp2):
	# If there is an update, output notification.
	saved = read_from_json("save.json")
	if not saved:
		return False
	names = None
	# Special
	if checked == "miui_c":
		names = ("MIUI China Stable ROM","MIUI China Developer ROM")
	elif checked == "miui_g":
		names = ("MIUI Global Stable ROM","MIUI Global Developer ROM")
	elif checked == "miui_mr":
		names = ("MIUI MultiRom Developer ROM China",
				"MIUI MultiRom Developer ROM Global")
	# Normal
	else:
		name = get_rom_name(checked)
	if names:
		flag = False
		for name in names:
			if (name in saved) and (saved[name] != temp2[name]):
				flag = print_update_info(name, saved[name], temp2[name])
		return flag
	else:
		if (name in saved) and (saved[name] != temp2[name]):
			return print_update_info(name, saved[name], temp2[name])
		return False

def print_update_info(name, old_name, new_name):
	print("\n%s\n"%("*" * 100))
	print("=== %s updated! Hurry to tell your friends :P\n"%name)
	print("=== Old version: %s\n"%old_name)
	print("=== New version: " + new_name)
	return True

def saved_update(name, version, saved):
	# Update dictionary
	if not saved:
		saved = {}
	saved[name] = version
	return saved

def save_to_json(ready_save_data, filename):
	# Save the dictionary to json
	with open(filename,'w') as savefile:
		json.dump(ready_save_data, savefile,
				sort_keys=True, indent=4, ensure_ascii=False)

def read_from_json(filename):
	# Read dictionary from json
	try:
		with open(filename,'r') as savefile:
			return json.load(savefile)
	except:
		try:
			os.remove(filename)
		finally:
			return None
