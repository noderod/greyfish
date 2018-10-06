#!/usr/bin/env python3

"""
BASICS

Returns user files or information about them
"""

import os, sys, shutil
from flask import Flask, request, jsonify, send_file
import base_functions as bf
from werkzeug.utils import secure_filename
import tarfile


app = Flask(__name__)
GREYFISH_FOLDER = os.environ['greyfish_path']+"/sandbox/"
CURDIR = dir_path = os.path.dirname(os.path.realpath(__file__)) # Current directory


# Checks if reef cloud storage is available
@app.route('/grey/status')
def api_operational():
    return 'External Greyfish cloud storage is available'


# Returns a json object of all the files obtained from the user
@app.route('/grey/all_user_files/<gkey>/<toktok>')
def all_user_files(toktok, gkey):

    IP_addr = request.environ['REMOTE_ADDR']
    if not bf.valid_key(gkey):
        bf.failed_login(gkey, IP_addr, toktok, "json-all-user-files")
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    bf.greyfish_log(IP_addr, toktok, "json summary", "all files")
    return jsonify(bf.structure_in_json(GREYFISH_FOLDER+'DIR_'+toktok))


# Returns the contents of an entire directory
@app.route('/grey/user_files/<gkey>/<toktok>/<DIR>')
def user_files(toktok, gkey, DIR=''):

    IP_addr = request.environ['REMOTE_ADDR']
    if not bf.valid_key(gkey):
        bf.failed_login(gkey, IP_addr, toktok, "json-user-dir")
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    # Accounts for users without a sandbox yet
    try:
        bf.greyfish_log(IP_addr, toktok, "json summary", "single dir", '/'.join(DIR.split('++')))
        return jsonify(bf.structure_in_json(GREYFISH_FOLDER+'DIR_'+toktok+'/'+'/'.join(DIR.split('++'))))

    except:
        return 'Sandbox not set-up, create a sandbox first'


# Uploads one file
# Directories must be separated by ++

@app.route("/grey/upload/<gkey>/<toktok>/<DIR>", methods=['POST'])
def result_upload(toktok, gkey, DIR=''):

    IP_addr = request.environ['REMOTE_ADDR']
    if not bf.valid_key(gkey):
        bf.failed_login(gkey, IP_addr, toktok, "upload-file")
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    file = request.files['file']
    fnam = file.filename

    # Avoids empty filenames and those with commas
    if fnam == '':
       return 'INVALID, no file uploaded'
    if ',' in fnam:
       return "INVALID, no ',' allowed in filenames"

    # Ensures no commands within the filename
    new_name = secure_filename(fnam)
    if not os.path.exists(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++'))):
        os.makedirs(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++')))

    bf.greyfish_log(IP_addr, toktok, "upload", "single file", '/'.join(DIR.split('++')), new_nam)
    file.save(os.path.join(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++')), new_name))
    return 'File succesfully uploaded to Greyfish'


# Deletes a file already present in the user
@app.route('/grey/delete_file/<gkey>/<toktok>/<FILE>/<DIR>')
def delete_file(toktok, gkey, FILE, DIR=''):

    IP_addr = request.environ['REMOTE_ADDR']
    if not bf.valid_key(gkey):
        bf.failed_login(gkey, IP_addr, toktok, "delete-file")
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    try:       
        os.remove(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++'))+'/'+str(FILE))
        bf.greyfish_log(IP_addr, toktok, "delete", "single file", '/'.join(DIR.split('++')), new_nam)
        return 'File succesfully deleted from Greyfish storage'

    except:
        return 'File is not present in Greyfish'


# Deletes a directory
@app.route("/grey/delete_dir/<gkey>/<toktok>/<DIR>")
def delete_dir(toktok, gkey, DIR):

    IP_addr = request.environ['REMOTE_ADDR']
    if not bf.valid_key(gkey):
        bf.failed_login(gkey, IP_addr, toktok, "delete-dir")
        return "INVALID key"

    try:
        shutil.rmtree(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++'))+'/')
        bf.greyfish_log(IP_addr, toktok, "delete", "single dir", '/'.join(DIR.split('++')))
        return "Directory deleted"
    except:
        return "User directory does not exist"


# Returns a file
@app.route('/grey/grey/<gkey>/<toktok>/<FIL>/<DIR>')
def grey_file(gkey, toktok, FIL, DIR=''):

    IP_addr = request.environ['REMOTE_ADDR']
    if not bf.valid_key(gkey):
        bf.failed_login(gkey, IP_addr, toktok, "download-file")
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    USER_DIR = GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++'))+'/'
    if str(FIL) not in os.listdir(USER_DIR):
       return 'INVALID, File not available'

    bf.greyfish_log(IP_addr, toktok, "download", "single file", '/'.join(DIR.split('++')), FIL)
    return send_file(USER_DIR+str(FIL))


# Uploads one directory, it the directory already exists, then it deletes it and uploads the new contents
# Must be a tar file
@app.route("/grey/upload_dir/<gkey>/<toktok>/<DIR>", methods=['POST'])
def upload_dir(gkey, toktok, DIR):

    IP_addr = request.environ['REMOTE_ADDR']
    if not bf.valid_key(gkey):
        bf.failed_login(gkey, IP_addr, toktok, "upload-dir")
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    file = request.files['file']
    fnam = file.filename

    # Avoids empty filenames and those with commas
    if fnam == '':
       return 'INVALID, no file uploaded'
    if ',' in fnam:
       return "INVALID, no ',' allowed in filenames"

    # Untars the file, makes a directory if it does not exist
    if ('.tar.gz' not in fnam) and ('.tgz' not in fnam):
        return 'ERROR: Compression file not accepted, file must be .tgz or .tar.gz'

    new_name = secure_filename(fnam)

    try:

        if os.path.exists(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++'))):
            shutil.rmtree(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++')))

        os.makedirs(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++')))
        file.save(os.path.join(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++')), new_name))
        tar = tarfile.open(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++'))+'/'+new_name)
        tar.extractall(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++')))
        tar.close()
        os.remove(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++'))+'/'+new_name)


    except:
        return "Could not open tar file" 

    bf.greyfish_log(IP_addr, toktok, "upload", "dir", '/'.join(DIR.split('++')))
    return 'Directory succesfully uploaded to Greyfish'


# Downloads a directory
# Equivalent to downloading the tar file, since they are both equivalent
@app.route('/grey/grey_dir/<gkey>/<toktok>/<DIR>')
def grey_dir(gkey, toktok, DIR=''):

    IP_addr = request.environ['REMOTE_ADDR']
    if not bf.valid_key(gkey):
        bf.failed_login(gkey, IP_addr, toktok, "download-dir")
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    USER_DIR = GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++'))+'/'

    if not os.path.exists(USER_DIR):
       return 'INVALID, Directory not available'

    os.chdir(USER_DIR)

    tar = tarfile.open("summary.tar.gz", "w:gz")
    for ff in os.listdir('.'):
      tar.add(ff)
    tar.close()

    os.chdir(CURDIR)

    bf.greyfish_log(IP_addr, toktok, "download", "dir", '/'.join(DIR.split('++')))
    return send_file(USER_DIR+"summary.tar.gz")


if __name__ == '__main__':
   app.run()
