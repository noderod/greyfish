#!/usr/bin/env python3

"""
BASICS

Returns user files or information about them
"""

import os, sys
from flask import Flask, request, jsonify, send_file
import base_functions as bf
from werkzeug.utils import secure_filename
import tarfile


app = Flask(__name__)
GREYFISH_FOLDER = os.environ['greyfish_path']+"/sandbox/"


# Checks if reef cloud storage is available
@app.route('/grey/status')
def api_operational():
    return 'External Greyfish cloud storage is available'


# Returns a json object of all the files obtained from the user
@app.route('/grey/all_user_files/<gkey>/<toktok>')
def all_user_files(toktok, gkey):

    if not bf.valid_key(gkey):
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    # Accounts for users without a sandbox yet
    try:
       return jsonify(bf.structure_in_json(GREYFISH_FOLDER+'/DIR_'+toktok))

    except:
       return 'Sandbox not set-up, create a sandbox first'


# Returns the contents of an entire directory
@app.route('/grey/user_files/<gkey>/<toktok>/<DIR>')
def all_user_files(toktok, gkey, DIR=''):

    if not bf.valid_key(gkey):
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    # Accounts for users without a sandbox yet
    try:
       return jsonify(bf.structure_in_json(GREYFISH_FOLDER+'/DIR_'+toktok+'/'+'/'.join(DIR.split(';'))))

    except:
       return 'Sandbox not set-up, create a sandbox first'


# Uploads one file
# Directories must be separated by ;

@app.route("/grey/upload/<gkey>/<toktok>/<DIR>", methods=['POST'])
def result_upload(toktok, gkey, DIR=''):

    if not bf.valid_key(gkey):
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    if request.method != 'POST':
       return 'INVALID, no file submitted'

    file = request.files['file']
    fnam = request.form['filename']

    # Avoids empty filenames and those with commas
    if file.filename == '':
       return 'INVALID, no file uploaded'
    if ',' in file.filename:
       return "INVALID, no ',' allowed in filenames"

    # Ensures no commands within the filename
    new_name = secure_filename(fnam)
    file.save(os.path.join(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split(';')), new_name))
    return 'File succesfully uploaded to Greyfish'


# Deletes a file already present in the user
@app.route('/grey/delete_file/<gkey>/<toktok>/<FILE>/<DIR>')
def delete_user_file(toktok, gkey, FILE, DIR=''):

    if not bf.valid_key(gkey):
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    try:       
       os.remove(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split(';'))+str(FILE))
       return 'File succesfully deleted from reef storage'

    except:
       return 'File is not present in Greyfish'


# Returns a file
@app.route('/grey/grey/<gkey>/<toktok>/<FIL>/<DIR>')
def results_file(gkey, toktok, FIL, DIR=''):

    if not bf.valid_key(gkey):
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    USER_DIR = GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split(';'))
    if str(FIL) not in os.listdir(USER_DIR):
       return 'INVALID, File not available'

    return send_file(USER_DIR+str(FIL))


# Uploads one ddirectory, it the directory already exists, then it deletes it and uploads the new contents
# Must be a tar file
@app.route("/grey/upload_dir/<gkey>/<toktok>/<DIR>")
def upload_dir(gkey, toktok, FIL, DIR):

    if not bf.valid_key(gkey):
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(GREYFISH_FOLDER):
       return 'INVALID, User directory does not exist'

    file = request.files['file']

    # Avoids empty filenames and those with commas
    if file.filename == '':
       return 'INVALID, no file uploaded'
    if ',' in file.filename:
       return "INVALID, no ',' allowed in filenames"

    # Untars the file, makes a directory if it does not exist
    if ('.tar.gz' not in file.filename) and ('.tgz' not in file.filename):
        return 'ERROR: Compression file not accepted, file must be .tgz or .tar.gz'

    try:
       tar = tarfile.open(file)
       tar.getmembers()
     except:
        tar.close()
        return "Tar cannot be opened"

    # Saves the file and deletes the rest
    tar.extractall(GREYFISH_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split(';')[:-1]))
    tar.close()

    return 'File succesfully uploaded to Greyfish'



if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 2000)
