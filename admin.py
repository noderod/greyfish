#!/usr/bin/env python3

"""
BASICS

Admin functionalities
"""



import os, sys, shutil
from flask import Flask, request, jsonify
import base_functions as bf
import tarfile


app = Flask(__name__)
GREYFISH_FOLDER = os.environ['greyfish_path']+"/sandbox/"





# Gets a list of all available users, comma-separated
@app.route('/grey/admin/users/all/names', methods=['POST'])
def all_usernames():

    if not request.is_json:
        return "INVALID: Request is not json"

    proposal = request.get_json()

    # Checks the required fields
    # self_ID (str) refers to the self-identity of the user, only useful for checking with Redis in case a temporary token is used 
    req_fields = ["key", "self_ID"]
    req_check = bf.l2_contains_l1(req_fields, proposal.keys())

    if req_check != []:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in req_check])


    gkey = proposal["key"]
    self_ID = proposal["self_ID"]

    IP_addr = request.environ['REMOTE_ADDR']
    if not bf.valid_key(gkey, self_ID):
        bf.failed_login(gkey, IP_addr, self_ID, "Get all usernames")
        return "INVALID key"

    bf.greyfish_admin_log(IP_addr, self_ID, "Get all usernames")
    # Checks the number of subdirectories, one assigned per user 
    return ','.join([f.path.replace(GREYFISH_FOLDER, '') for f in os.scandir(GREYFISH_FOLDER) if f.is_dir()])    




if __name__ == '__main__':
   app.run()


