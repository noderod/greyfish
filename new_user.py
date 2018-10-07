#!/usr/bin/env python3

"""
BASICS

Creates a new user, specified by their token
If the user already exists, an error result is returned
"""

import os, shutil
from flask import Flask, request
import base_functions as bf
from urllib.parse import unquote


app = Flask(__name__)
GREYFISH_FOLDER = os.environ['greyfish_path']+"/sandbox/"
hugo = bf.idb_writer('greyfish')


# toktok (str): User token
@app.route("/greyfish/api/users/create_user/<toktok>")
def create_user(toktok):

    try:
        gkey = request.form['gkey']
    except:
        return "INVALID input, greyfish key not provided"

    tokotk = unquote(toktok)

    # Gets the IP address
    IP_addr = request.environ['REMOTE_ADDR']
    if not bf.valid_key(gkey):
        # Records all failed logins
        bf.failed_login(gkey, IP_addr, toktok, "create-new-user")
        return "INVALID key, cannot create a new user"

    try:
        os.makedirs(GREYFISH_FOLDER+'DIR_'+str(toktok))
        hugo.write_points([{
                            "measurement":"signup",
                            "tags":{
                                    "id":toktok,
                                    },
                            "time":bf.timformat(),
                            "fields":{
                                    "client-IP":IP_addr
                                    }
                            }])

        return "Greyfish cloud storage now available"
    except:
        return "User already has an account"


# Deletes an entire user directory
@app.route("/greyfish/api/users/delete_user/<toktok>")
def delete_user(toktok, gkey):

    try:
        gkey = request.form['gkey']
    except:
        return "INVALID input, greyfish key not provided"

    tokotk = unquote(toktok)

    IP_addr = request.environ['REMOTE_ADDR']

    if not bf.valid_key(gkey):
        bf.failed_login(gkey, IP_addr, toktok, "delete-user")
        return "INVALID key, cannot create a new user"

    try:
        shutil.rmtree(GREYFISH_FOLDER+'DIR_'+str(toktok))
        hugo.write_points([{
                    "measurement":"delete_account",
                    "tags":{
                            "id":toktok,
                            },
                    "time":bf.timformat(),
                    "fields":{
                            "client-IP":IP_addr
                            }
                    }])

        return "User files and data have been completely deleted"
    except:
        return "User does not exist"


if __name__ == '__main__':
   app.run()
