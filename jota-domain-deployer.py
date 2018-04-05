#!/usr/bin/env python3
"""
Author        :Julio Sanz
Website       :www.elarraydejota.com
Email         :juliojosesb@gmail.com
Description   :Deploy to remote Server Group (domain mode) using Python Requests library
License       :GPLv3
"""

import os
import argparse
import ntpath
import requests
import json
from requests.auth import HTTPDigestAuth


def do_deploy(args):
    
    user = args.user
    password = args.password
    destination = args.destination
    server_group = args.servergroup
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

    r_content = requests.post(destination+'/management/add-content', files=files, auth=HTTPDigestAuth(user, password))
    json_data = json.loads(r_content.text)
    v_bytes_value = json_data['result']['BYTES_VALUE']
    print ("> Package name {}".format(package))
    print ("> Added content with hash \"{}\"".format(v_bytes_value))

    data_repository = '{"content":[{"hash": {"BYTES_VALUE" : "%s"}}], \
    "address": [{"deployment":"%s"}], \"operation":"add"}' % (v_bytes_value,package)
    data_deploy = '{"content":[{"hash": {"BYTES_VALUE" : "%s"}}], \
    "address": [{"server-group":"%s"},{"deployment":"%s"}], \"operation":"add", "enabled":"true"}' % (v_bytes_value,server_group,package)

    # Add package to repository
    print ("> Added package {} to repository".format(package))
    requests.post(destination+'/management', auth=HTTPDigestAuth(user, password), headers=headers, data=(data_repository))

    # Deploy (enable) package
    print ("> Deploying package {} to Server Group {}".format(package,server_group))
    r_deploy = requests.post(destination+'/management', auth=HTTPDigestAuth(user, password), \
                             headers=headers, data=(data_deploy))
    print ("> Result:")
    print (r_deploy.text)

 
if __name__ == '__main__':
    # Initial argument parser
    parser = argparse.ArgumentParser(description="Deploy to remote Jboss Server Group (domain mode)")
    required = parser.add_argument_group("Required arguments")
    required.add_argument('-u', '--user', required=True, help='Jboss user with administrative privileges')
    required.add_argument('-p', '--password', required=True, help='Password for admin user')
    required.add_argument('-d', '--destination', required=True, metavar='http(s)://IP:PORT' , help='Destination IP')
    required.add_argument('-sg', '--servergroup', required=True, help='Destination Server Group')
    required.add_argument('-pkg', '--package', required=True, metavar='/path/to/package', help='Full path to package')
    args = parser.parse_args()
    
    # Function calls
    do_deploy(args)   