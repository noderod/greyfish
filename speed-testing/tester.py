"""
BASICS

Tests upload and/or download speeds for a greyfish setup
"""


import argparse
import os
import requests
import server_props as sp
import time



parser = argparse.ArgumentParser()

parser.add_argument("-u", "--upload", default=False, help="File is tested for download", action="store_true")
parser.add_argument("-d", "--download", default=False, help="Adds download size (MB)", action="store_true")
parser.add_argument("-s", "--size", required=True, help="Adds file size (MB)", type=int)
args = parser.parse_args()

file_size = args.size


# Creates an empty file
with open("testfile", "wb") as f:
    f.write(os.urandom(file_size*1000000))


if args.upload:
    t1 = time.time()
    r = requests.post("http://"+sp.server_IP+":2000/grey/upload/"+sp.greyfish_key+"/"+sp.user+"/test", files={"file": open("testfile","rb")})
    t2 = time.time()
    print("U,"+ str(file_size)+"," +str(t2-t1))


# Requires the file to be present in the server
if args.download:
    t1 = time.time()
    r = requests.get("http://"+sp.server_IP+":2000/grey/create_user/"+sp.greyfish_key+"/"+sp.user+"/test/testfile")
    with open("download_test", "wb") as f:
        f.write(r.content)

    t2 = time.time()
    os.remove("download_test")
    print("D,"+ str(file_size)+","+ str(t2-t1))


# Deletes the empty file
os.remove("testfile")
