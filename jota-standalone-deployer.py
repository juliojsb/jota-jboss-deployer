#!/usr/bin/env python3
"""
Author        :Julio Sanz
Website       :www.elarraydejota.com
Email         :juliojosesb@gmail.com
Description   :Deploy to remote Jboss standalone node using Python Requests library
License       :GPLv3
"""

import os
import ntpath
import requests
import json
import argparse
from requests.auth import HTTPDigestAuth


def do_deploy(args):
    
    user = args.user
    password = args.password
    destination = args.destination
    full_path = args.package

    if os.name == 'nt':
        package = os.path.basename(full_path)
    if os.name == 'posix':
        package = ntpath.basename(full_path)
    
    files = {
        'file': (full_path, open(full_path, 'rb')),
    }
    headers = {
        'Content-Type': 'application/json', 'Accept': 'text/plain'
    }    

    # Add content    
    r_content = requests.post(destination+'/management/add-content', files=files, auth=HTTPDigestAuth(user, password))

    json_data = json.loads(r_content.text)
    v_bytes_value = json_data['result']['BYTES_VALUE']
    print ("> Package name {}".format(package))
    print ("> Added content with hash \"{}\"".format(v_bytes_value))

    # Enable deployment
    data = '{"content":[{"hash": {"BYTES_VALUE" : "%s"}}], \
    "address": [{"deployment":"%s"}], \"operation":"add", "enabled":"true"}' % (v_bytes_value,package)
       
    print ("> Deploying package {} to node {}".format(package,destination))
    print ("> Result:")
    
    r_deploy = requests.post(destination+'/management', auth=HTTPDigestAuth(user, password), \
                             headers=headers, data=(data))

    print (r_deploy.text)


if __name__ == '__main__':
    # Initial argument parser
    parser = argparse.ArgumentParser(description="Deploy to remote Jboss standalone node")
    required = parser.add_argument_group("Required arguments")
    required.add_argument('-u', '--user', required=True, help='Jboss user with administrative privileges')
    required.add_argument('-p', '--password', required=True, help='Password for admin user')
    required.add_argument('-d', '--destination', required=True, metavar='http(s)://IP:PORT' , help='Destination IP')
    required.add_argument('-pkg', '--package', required=True, metavar='/path/to/package', help='Full path to package')
    args = parser.parse_args()
    
    # Function calls
    do_deploy(args)   