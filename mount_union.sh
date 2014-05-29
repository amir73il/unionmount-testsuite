#!/bin/bash

. ./settings.inc

if [ "$TEST_OVERLAYFS" != 1 ]
then
    /root/util-linux-union/mount/mount -i -t tmpfs upper_layer $union_mntroot -o union || exit $?
    sync || exit $?

    upper_fs=`stat -c %D $testdir`
    if [ x$lower_fs == x$upper_fs ]
    then
	echo "Upper ($upper_fs) and lower ($lower_fs) shouldn't be the same" >&2
	exit 1
    fi
else
    mount -t tmpfs upper_layer $upper_mntroot || exit $?
    upperdir=$upper_mntroot/upper
    workdir=$upper_mntroot/work
    mkdir $upperdir || exit $?
    mkdir $workdir || exit $?
    mount -t overlayfs overlayfs $union_mntroot \
	  -olowerdir=$lower_mntroot,upperdir=$upperdir,workdir=$workdir || exit $?
fi
