#!/usr/bin/env python3

import os
import sys
import ntpath
import requests
import json
from requests.auth import HTTPDigestAuth


#
# GLOBAL VARIABLES
#

user = sys.argv[1]
password = sys.argv[2]
destination = sys.argv[3]
full_path = sys.argv[4]
server_group = sys.argv[5]

if os.name == 'nt':
    package = os.path.basename(sys.argv[4])

if os.name == 'posix':
    package = ntpath.basename(sys.argv[4])

v_bytes_value = ""


#
# FUNCTIONS
#

def add_content():
    files = {
        'file': (full_path, open(full_path, 'rb')),
    }

    r = requests.post(destination+'/management/add-content', files=files, auth=HTTPDigestAuth(user, password))
    #print (r.text)
    #print (r.headers['content-type'])
    json_data = json.loads(r.text)
    v_bytes_value = json_data['result']['BYTES_VALUE']
    #print (v_bytes_value)
    print ("> Package name {}".format(package))
    print ("> Added content with hash \"{}\"".format(v_bytes_value))
    do_deployment(v_bytes_value)

def do_deployment(v_bytes_value):
    headers = {
        'Content-Type': 'application/json', 'Accept': 'text/plain'
    }

    data_repository = '{"content":[{"hash": {"BYTES_VALUE" : "%s"}}], \
    "address": [{"deployment":"%s"}], \"operation":"add"}' % (v_bytes_value,package)

    data_deploy = '{"content":[{"hash": {"BYTES_VALUE" : "%s"}}], \
    "address": [{"server-group":"%s"},{"deployment":"%s"}], \"operation":"add", "enabled":"true"}' % (v_bytes_value,server_group,package)

    # Add package to repository
    print ("> Added package {} to Repository".format(package))
    response = requests.post(destination+'/management', auth=HTTPDigestAuth(user, password), \
                             headers=headers, data=(data_repository))

    # Deploy (enable) package
    print ("> Deploying package {} to Server Group {}".format(package,server_group))
    response = requests.post(destination+'/management', auth=HTTPDigestAuth(user, password), \
                             headers=headers, data=(data_deploy))
    print ("> Result:")
    print response.text

    
#
# MAIN
#
 
if __name__ == '__main__':
    add_content()