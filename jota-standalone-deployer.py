#!/usr/bin/env python3
"""
Author        :Julio Sanz
Website       :www.elarraydejota.com
Email         :juliojosesb@gmail.com
Description   :Deploy to remote Jboss standalone node using Python Requests library
License       :GPLv3
"""

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

    data = '{"content":[{"hash": {"BYTES_VALUE" : "%s"}}], \
    "address": [{"deployment":"%s"}], \"operation":"add", "enabled":"true"}' % (v_bytes_value,package)
       
    #print (json.dumps(data))
    print ("> Deploying package {} to node {}".format(package,destination))
    print ("> Result:")
    
    response = requests.post(destination+'/management', auth=HTTPDigestAuth(user, password), \
                             headers=headers, data=(data))

    #print response
    print response.text

    
#
# MAIN
#
 
if __name__ == '__main__':
    add_content()
