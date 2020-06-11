#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output
import os
import random
import string
import sys


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == "__main__":

    os.environ["CONAN_PRINT_RUN_COMMANDS"] = "True"
    os.environ["CONAN_RETRY"] = "10"
    os.environ["CONAN_RETRY_WAIT"] = "10"
    os.system("conan profile new ./ci-profile")

    if 'CONAN_BASE_PROFILE_OS' in os.environ:
        os.system("conan profile update settings.os=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_OS'])

    if 'CONAN_BASE_PROFILE_OS_API' in os.environ:
        os.system(
            "conan profile update settings.os.api_level=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_OS_API'])

    if 'CONAN_BASE_PROFILE_OS_VERSION' in os.environ:
        os.system("conan profile update settings.os.version=\"%s\" ./ci-profile" % os.environ[
            'CONAN_BASE_PROFILE_OS_VERSION'])

    if 'CONAN_BASE_PROFILE_OSBUILD' in os.environ:
        os.system(
            "conan profile update settings.os_build=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_OSBUILD'])

    if 'CONAN_BASE_PROFILE_ARCH' in os.environ:
        os.system("conan profile update settings.arch=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_ARCH'])

    if 'CONAN_BASE_PROFILE_ARCHBUILD' in os.environ:
        os.system(
            "conan profile update settings.arch_build=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_ARCHBUILD'])

    if 'CONAN_BASE_PROFILE_COMPILER' in os.environ:
        os.system(
            "conan profile update settings.compiler=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_COMPILER'])

    if 'CONAN_BASE_PROFILE_COMPILER_VERSION' in os.environ:
        os.system("conan profile update settings.compiler.version=\"%s\" ./ci-profile" % os.environ[
            'CONAN_BASE_PROFILE_COMPILER_VERSION'])

    if 'CONAN_BASE_PROFILE_COMPILER_LIBCXX' in os.environ:
        os.system("conan profile update settings.compiler.libcxx=\"%s\" ./ci-profile" % os.environ[
            'CONAN_BASE_PROFILE_COMPILER_LIBCXX'])

    if 'CONAN_BASE_PROFILE_BUILDTYPE' in os.environ:
        os.system(
            "conan profile update settings.build_type=\"%s\" ./ci-profile" % os.environ['CONAN_BASE_PROFILE_BUILDTYPE'])

    if 'CONAN_OPTIONS' in os.environ:
        for option in os.environ['CONAN_OPTIONS'].split(','):
            os.system("conan profile update options.%s ./ci-profile" % option)

    user_name = "user"
    user_channel = "testing"
    if 'CONAN_USERNAME' in os.environ:
        user_name = os.environ['CONAN_USERNAME']

    if 'CONAN_CHANNEL' in os.environ:
        user_channel = os.environ['CONAN_CHANNEL']

    for remote in os.environ['CONAN_REMOTES'].split(','):
        rep_name = randomString()
        print("Adding remote: " + rep_name + " url: " + remote)
        os.system("conan remote add -f %s %s" % (rep_name, remote))

    version = check_output(["conan", "inspect", ".", "-a", "version"]).decode("ascii").rstrip()
    name = check_output(["conan", "inspect", ".", "-a", "name"]).decode("ascii").rstrip()
    package_ref = "%s/%s" % (user_name, user_channel)
    package_name = "%s/%s@%s" % (name[6:], version[9:], package_ref)

    print("Building recipe with reference: " + package_ref)
    os.system("conan create . %s/%s -pr ./ci-profile -b outdated" % (user_name, user_channel))

    print("Installing artifacts")
    os.system("conan install %s -pr ./ci-profile" % package_name)
