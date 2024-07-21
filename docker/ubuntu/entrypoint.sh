#!/bin/sh

TMPFILE=$(mktemp /tmp/cmd-XXXXXXXX.sh)
echo "#!/bin/bash\nconan profile detect -vquiet\n$@" > $TMPFILE
exec bash -e $TMPFILE
