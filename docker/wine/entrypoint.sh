#!/bin/sh

TMPFILE=$(mktemp /tmp/cmd-XXXXXXXX.bat)
echo "$@" > $TMPFILE && . /opt/mkuserwineprefix && wine64 cmd /S /C $TMPFILE
