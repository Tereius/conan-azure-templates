#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output, check_call
import os
import random
import string
import sys
import json


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


if __name__ == "__main__":

    print("Using Python version")
    print(sys.version)

    host_profile_path = None
    check_call("conan profile detect")
    check_call("conan config install global.conf")
    check_call("conan config install -tf extensions/hooks hook_clean_cache.py")

    if 'CONAN_HOST_PROFILE_PATH' in os.environ:
        host_profile_path = os.environ['CONAN_HOST_PROFILE_PATH']

    recipe_path = "."
      
    if 'CONAN_RECIPE_PATH' in os.environ:
        recipe_path = os.environ['CONAN_RECIPE_PATH']

    if 'CONAN_REMOTES' in os.environ:
        for remote in os.environ['CONAN_REMOTES'].split(','):
            rep_name = randomString()
            print("Adding remote: " + rep_name + " url: " + remote)
            check_call("conan remote add --index 0 --force %s %s" % (rep_name, remote))

    name = json.loads(check_output(["conan", "inspect", recipe_path, "-f", "json"]).decode("ascii"))["name"]
    version = json.loads(check_output(["conan", "inspect", recipe_path, "-f", "json"]).decode("ascii"))["version"]
    user = json.loads(check_output(["conan", "inspect", recipe_path, "-f", "json"]).decode("ascii"))["user"]
    cannel = json.loads(check_output(["conan", "inspect", recipe_path, "-f", "json"]).decode("ascii"))["channel"]

    package_ref = "%s/%s@%s/%s" % (name, version, user, cannel)

    print("Building recipe: " + package_name)
    check_call("conan create %s -pr:h \"%s\" -tf "" -u -b missing" % (recipe_path, profile_path, build_profile_path), shell=True)
    print("-----Finished-----")
