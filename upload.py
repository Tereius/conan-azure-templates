#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output
import os
import random
import string


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == "__main__":

    user_name = "user"
    user_channel = "testing"
    upload_all = False
    if 'CONAN_USERNAME' in os.environ:
        user_name = os.environ['CONAN_USERNAME']

    if 'CONAN_CHANNEL' in os.environ:
        user_channel = os.environ['CONAN_CHANNEL']
    
    if 'UPLOAD_ALL' in os.environ:
        upload_all = True
    
    if not 'CONAN_UPLOAD' in os.environ:
        print('Missing "CONAN_UPLOAD" env. variable')
        quit(1)

    rep_name = randomString()

    print("Adding remote for upload: " + os.environ['CONAN_UPLOAD'])
    os.system(["conan", "remote", "add", "-f", rep_name, os.environ['CONAN_UPLOAD']])
    try:
        os.system(["conan", "user", "-p", os.environ['CONAN_PASSWORD'], "-r", rep_name, os.environ['CONAN_LOGIN_USERNAME']])
    except:
        print("Warning: Couldn't set user credentials for remote")
    version = check_output(["conan", "inspect", ".", "-a", "version"]).decode("ascii").rstrip()
    name = check_output(["conan", "inspect", ".", "-a", "name"]).decode("ascii").rstrip()
    package_ref = "%s/%s" % (user_name, user_channel)
    package_name = "%s/%s@%s" % (name[6:], version[9:], package_ref)
    print("Exporting recipe with reference: " + package_ref)
    check_call(["conan", "export", ".", package_ref])
    if upload_all:
        print("Uploading recipe and package: " + package_name)
        check_call(["conan", "upload", package_name, "-r", rep_name, "--all", "--retry", "3", "--retry-wait", "240"])
    else:
        print("Uploading recipe: " + package_name)
        check_call(["conan", "upload", package_name, "-r", rep_name, "--retry", "3", "--retry-wait", "240"]) 
