#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import *
from bs4 import BeautifulSoup
import os
import json
import random
import ssl

import rom_list

def ua_open(urll, ua_type = None, ssl_flag = None):
    # Use browser proxy to parse web pages
    if ua_type == None:
        # Randomly select the browser UA
        ua_type = random.randint(1,4)
    if ua_type == 1:
        ua = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
              "/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 "
              "Safari/537.36")
    elif ua_type== 2:
        ua = ("Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us)"
              " AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 "
              "Safari/534.50")
    elif ua_type == 3:
        ua = ("Opera/9.80 (Windows NT 6.1; U; en) "
              "Presto/2.8.131 Version/11.11")
    elif ua_type == 4:
        ua = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) "
              "Gecko/20100101 Firefox/4.0.1")
    headers = {}
    headers["User-Agent"] = ua
    try:
        req = Request(url = urll, headers = headers)
        if ssl_flag:
            context = ssl._create_unverified_context()
            with urlopen(req, context=context) as xmldata:
                return xmldata.read()
        else:
            with urlopen(req) as xmldata:
                return xmldata.read()
    except:
        return
    finally:
        if ssl_flag:
            del context

def de_open(urll, ssl_flag = None):
    # The general method of parsing the page
    try:
        if ssl_flag:
            context = ssl._create_unverified_context()
            with urlopen(urll, context=context) as xmldata:
                return xmldata.read()
        else:
            with urlopen(urll) as xmldata:
                return xmldata.read()
    except:
        return
    finally:
        if ssl_flag:
            del context

def select_bs4_parser():
    try:
        import lxml
        return "lxml"
    except ModuleNotFoundError:
        try:
            import html5lib
            return "html5lib"
        except ModuleNotFoundError:
            return

def get_bs(urll, bs4_parser):
    # Get BeautifulSoup for the source of the page
    if not urll:
        return
    try:
        return BeautifulSoup(urll, bs4_parser)
    except:
        return

def open_failed(real_name = None):
    if real_name:
        print("\n%s:\n"%real_name)
    print("*** Access failed or request timeout!")

def analyze_failed(real_name = None):
    if real_name:
        print("\n%s:\n"%real_name)
    print("*** Parsing failed! Please tell author to fix this error!")

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
    # Temporarily generate a "roms" object
    roms = rom_list.Rom_List()
    try:
        return roms.get_name(name)
    finally:
        del roms

def out_put(fast_flag, name, fversion, build_info):
    # Output check results
    print_info = ["None" for i in range(10)]
    print_info[0] = "=== The latest version:\n\n    " + fversion
    for key, value in build_info.items():
        if key == "build_type":
            print_info[1] = "\n=== Build type:\n\n    " + value
        elif key == "build_version":
            print_info[2] = "\n=== Build version:\n\n    " + value
        elif key == "fdate":
            print_info[3] = "\n=== Updated:\n\n    " + value
        elif key == "update_log":
            print_info[4] = "\n=== Changelog:\n\n    " + value
        elif key == "fmd5":
            print_info[5] = "\n=== MD5:\n\n    " + value
        elif key == "fsha256":
            print_info[6] = "\n=== sha256:\n\n    " + value
        elif key == "fsha1":
            print_info[7] = "\n=== sha1:\n\n    " + value
        elif key == "flink":
            print_info[8] = "\n=== Download link:\n\n    " + value
        elif key == "fsize":
            print_info[9] = "\n=== Size:\n\n    " + value
    for info in print_info:
        if info == "None":
            continue
        print(info)
    saved = None
    if fast_flag == False:
        saved = read_from_json("save.json")
    return saved_update(get_rom_name(name), fversion, saved)

def check_for_update(checked, temp2, term_cols):
    # If there is an update, output notification.
    saved = read_from_json("save.json")
    if not saved:
        return
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
        names = None
    if names:
        flag = False
        for name in names:
            if (name in saved) and (saved[name] != temp2[name]):
                flag = print_update_info(name, term_cols,
                                         saved[name], temp2[name])
        return flag
    else:
        if (name in saved) and (saved[name] != temp2[name]):
            return print_update_info(name, term_cols,
                                      saved[name], temp2[name])
        return

def print_update_info(name, term_cols, old_name, new_name):
    print("\n%s\n"%("*" * 2 * term_cols))
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
    # Remove error items
    ekey = []
    roms = rom_list.Rom_List()
    for key in ready_save_data.keys():
        if key not in roms.name_all:
            ekey.append(key)
    for k in ekey:
        del ready_save_data[k]
    # Save the dictionary to json
    try:
        with open(filename,"w") as savefile:
            json.dump(ready_save_data, savefile,
                      sort_keys=True, indent=4, ensure_ascii=False)
    # Debug
    except:
        print(ready_save_data)
        raise Exception("Write json failed!")
    finally:
        del roms

def read_from_json(filename):
    # Read dictionary from json
    try:
        with open(filename,"r") as savefile:
            return json.load(savefile)
    except:
        try:
            os.remove(filename)
        finally:
            return
