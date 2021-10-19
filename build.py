#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output, check_call
import os
import random
import string
import sys


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


if __name__ == "__main__":

    print("Using Python version")
    print(sys.version)

    os.environ["CONAN_PRINT_RUN_COMMANDS"] = "True"
    os.environ["CONAN_RETRY"] = "10"
    os.environ["CONAN_RETRY_WAIT"] = "10"
    profile_path = "./ci-profile"
    build_profile_path = None
    os.system("conan profile new ./ci-profile")

    if 'CONAN_BASE_PROFILE' in os.environ:
        profile_path = os.environ['CONAN_BASE_PROFILE']

    if 'CONAN_BASE_PROFILE_PATH' in os.environ:
        profile_path = os.environ['CONAN_BASE_PROFILE_PATH']

    if 'CONAN_BUILD_PROFILE' in os.environ:
        build_profile_path = os.environ['CONAN_BUILD_PROFILE']

    if 'CONAN_BASE_PROFILE_OS' in os.environ:
        os.system(
            "conan profile update settings.os=\"%s\" \"%s\"" % (os.environ['CONAN_BASE_PROFILE_OS'], profile_path))

    if 'CONAN_BASE_PROFILE_OS_API' in os.environ:
        os.system(
            "conan profile update settings.os.api_level=\"%s\" \"%s\"" % (
                os.environ['CONAN_BASE_PROFILE_OS_API'], profile_path))

    if 'CONAN_BASE_PROFILE_OS_VERSION' in os.environ:
        os.system("conan profile update settings.os.version=\"%s\" \"%s\"" % (os.environ[
                                                                                  'CONAN_BASE_PROFILE_OS_VERSION'],
                                                                              profile_path))

    if 'CONAN_BASE_PROFILE_OSBUILD' in os.environ:
        os.system(
            "conan profile update settings.os_build=\"%s\" \"%s\"" % (
                os.environ['CONAN_BASE_PROFILE_OSBUILD'], profile_path))

    if 'CONAN_BASE_PROFILE_ARCH' in os.environ:
        os.system(
            "conan profile update settings.arch=\"%s\" \"%s\"" % (os.environ['CONAN_BASE_PROFILE_ARCH'], profile_path))

    if 'CONAN_BASE_PROFILE_ARCHBUILD' in os.environ:
        os.system(
            "conan profile update settings.arch_build=\"%s\" \"%s\"" % (
                os.environ['CONAN_BASE_PROFILE_ARCHBUILD'], profile_path))

    if 'CONAN_BASE_PROFILE_COMPILER' in os.environ:
        os.system(
            "conan profile update settings.compiler=\"%s\" \"%s\"" % (
                os.environ['CONAN_BASE_PROFILE_COMPILER'], profile_path))

    if 'CONAN_BASE_PROFILE_COMPILER_VERSION' in os.environ:
        os.system("conan profile update settings.compiler.version=\"%s\" \"%s\"" % (os.environ[
                                                                                        'CONAN_BASE_PROFILE_COMPILER_VERSION'],
                                                                                    profile_path))

    if 'CONAN_BASE_PROFILE_COMPILER_LIBCXX' in os.environ:
        os.system("conan profile update settings.compiler.libcxx=\"%s\" \"%s\"" % (os.environ[
                                                                                       'CONAN_BASE_PROFILE_COMPILER_LIBCXX'],
                                                                                   profile_path))

    if 'CONAN_BASE_PROFILE_BUILDTYPE' in os.environ:
        os.system(
            "conan profile update settings.build_type=\"%s\" \"%s\"" % (
                os.environ['CONAN_BASE_PROFILE_BUILDTYPE'], profile_path))

    if 'CONAN_OPTIONS' in os.environ:
        for option in os.environ['CONAN_OPTIONS'].split(','):
            os.system("conan profile update options.%s \"%s\"" % (option, profile_path))

    user_name = "user"
    user_channel = "testing"
    package_name = ""
    recipe_path = "."
    if 'CONAN_USERNAME' in os.environ:
        user_name = os.environ['CONAN_USERNAME']

    if 'CONAN_CHANNEL' in os.environ:
        user_channel = os.environ['CONAN_CHANNEL']
        
    if 'CONAN_PACKAGE_NAME' in os.environ:
        package_name = os.environ['CONAN_PACKAGE_NAME']
        
    if 'CONAN_RECIPE_PATH' in os.environ:
        recipe_path = os.environ['CONAN_RECIPE_PATH']

    if 'CONAN_REMOTES' in os.environ:
        for remote in os.environ['CONAN_REMOTES'].split(','):
            rep_name = randomString()
            print("Adding remote: " + rep_name + " url: " + remote)
            os.system("conan remote add -f %s %s" % (rep_name, remote))

    if not package_name:
        version = check_output(["conan", "inspect", recipe_path, "-a", "version"]).decode("ascii").rstrip()
        name = check_output(["conan", "inspect", recipe_path, "-a", "name"]).decode("ascii").rstrip()
        package_ref = "%s/%s" % (user_name, user_channel)
        package_name = "%s/%s@%s" % (name[6:], version[9:], package_ref)

    print("Building recipe: " + package_name)
    if build_profile_path is not None:
        print("-----Building dependencies (host-, build-profile)-----")
        check_call("conan install %s %s -pr:h \"%s\" -pr:b \"%s\" -b outdated" % (recipe_path, package_name, profile_path, build_profile_path), shell=True)
        os.system("conan remove \"*\" -s -b -f") # Clean up the conan cache to free some memory
        print("-----Building recipe (host-, build-profile)-----")
        check_call("conan create %s %s -pr:h \"%s\" -pr:b \"%s\" -tf None -b outdated" % (recipe_path, package_name, profile_path, build_profile_path), shell=True)
        print("-----Building recipe finished (host-, build-profile)-----")
    else:
        print("-----Building dependencies (single profile)-----")
        check_call("conan install %s %s -pr \"%s\" -b outdated" % (recipe_path, package_name, profile_path), shell=True)
        os.system("conan remove \"*\" -s -b -f") # Clean up the conan cache to free some memory
        print("-----Building recipe (single profile)-----")
        check_call("conan create %s %s -pr \"%s\" -tf None -b outdated" % (recipe_path, package_name, profile_path), shell=True)
        print("-----Building recipe finished (single profile)-----")

    if 'SKIP_INSTALL_ARTIFACTS' not in os.environ:
        print("-----Installing artifacts-----")
        check_call("conan install %s -pr \"%s\"" % (package_name, profile_path), shell=True)
    print("-----Finished-----")
