#!/bin/bash

if [ "$TEST_OVERLAYFS" != 1 ]
then
    lower_mntroot=/mnt
    union_mntroot=/mnt
else
    lower_mntroot=/lower
    upper_mntroot=/upper
    union_mntroot=/mnt
fi

openfile=/usr/local/bin/open-file
fsop=/usr/local/bin/fs-op

#
lowerdir=$lower_mntroot/a
testdir=$union_mntroot/a

if [ "$TERMSLASH" == "1" ]
then
    termslash=/
else
    termslash=
fi
