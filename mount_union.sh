#!/bin/bash

. ./settings.inc

/root/util-linux-union/mount/mount -i -t tmpfs none $mntroot -o union || exit $?
sync || exit $?

upper_fs=`stat -c %D $testdir`
if [ x$lower_fs == x$upper_fs ]
then
	echo "Upper ($upper_fs) and lower ($lower_fs) shouldn't be the same" >&2
	exit 1
fi
