"""
BASICS

Creates a greyfish user
"""


import requests
import server_props as sp



r = requests.get("http://"+sp.server_IP+":2003/grey/create_user/"+sp.greyfish_key+"/"+sp.user)
print(r.text)
