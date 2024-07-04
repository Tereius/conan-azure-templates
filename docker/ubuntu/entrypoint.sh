#!/bin/sh

conan profile detect -vquiet
exec bash -c "$@"
