#!/usr/bin/env python3
"""
BASICS

Implements communication between end user calling greyfish and the other nodes
"""


from flask import Flask, request
import os, shutil
import redis

import base_functions as bf


app = Flask(__name__)
GREYFISH_FOLDER = os.environ['greyfish_path']+"/sandbox/"


URL_BASE = os.environ["URL_BASE"]
REDIS_AUTH = os.environ["REDIS_AUTH"]


# toktok (str): User token
@app.route("/grey/create_user", methods=['POST'])
def create_user():

    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    [error_occurs, missing_fields] = bf.error__l2_contains_l1(ppr.keys(), ["user_id", "gkey"])

    if error_occurs:
        return "INVALID: Lacking the following json fields to be read: "+missing_fields

    toktok = ppr["user_id"]
    gkey = ppr["gkey"]

    # Gets the IP address
    IP_addr = request.environ['REMOTE_ADDR']
    if not bf.valid_key(gkey, toktok):
        # Records all failed logins
        bf.failed_login(gkey, IP_addr, toktok, "create-new-user")
        return "INVALID key, cannot create a new user"

    user_action = bf.idb_writer('greyfish')

    # Stores usernames in Redis since this will be faster to check in the future
    r_users = redis.Redis(host=URL_BASE, password=os.environ['REDIS_AUTH'], db=5)
    if r_users.get(toktok) != None:
        return "User already has an account"

    try:
        user_action.write_points([{
                            "measurement":"user_action",
                            "tags":{
                                    "id":toktok,
                                    "action":"signup"
                                    },
                            "time":bf.timformat(),
                            "fields":{
                                    "client-IP":IP_addr
                                    }
                            }])

        r_users.set(toktok, "Active")

        return "Greyfish cloud storage now available"
    except:
        return "Server Error: Could not connect to database"


# Deletes an entire user directory
@app.route("/grey/delete_user", methods=['POST'])
def delete_user():

    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    [error_occurs, missing_fields] = bf.error__l2_contains_l1(ppr.keys(), ["user_id", "gkey"])

    if error_occurs:
        return "INVALID: Lacking the following json fields to be read: "+missing_fields

    toktok = ppr["user_id"]
    gkey = ppr["gkey"]

    IP_addr = request.environ['REMOTE_ADDR']

    if not bf.valid_key(gkey, toktok):
        bf.failed_login(gkey, IP_addr, toktok, "delete-user")
        return "INVALID key, cannot create a new user"

    user_action = bf.idb_writer('greyfish')

    r_users = redis.Redis(host=URL_BASE, password=os.environ['REDIS_AUTH'], db=5)
    if r_users.get(toktok) == None:
        return "User does not exist"

    try:
        user_action.write_points([{
                    "measurement":"user_action",
                    "tags":{
                            "id":toktok,
                            "action":"delete account"
                            },
                    "time":bf.timformat(),
                    "fields":{
                            "client-IP":IP_addr
                            }
                    }])

        r_users.delete(toktok)

        return "User files and data have been completely deleted"
    except:
        return "Server Error: Could not connect to database"


if __name__ == '__main__':
   app.run()
