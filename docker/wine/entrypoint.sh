#!/bin/sh

TMPFILE=$(mktemp /tmp/cmd-XXXXXXXX.bat)
echo "@echo off\r\nset Python_ROOT_DIR=C:\\Python\r\n$@" > $TMPFILE && . /opt/mkuserwineprefix && wine64 cmd /S /C $TMPFILE
