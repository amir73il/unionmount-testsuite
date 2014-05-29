#!/bin/bash

. ./settings.inc
. ./tool_box.inc

umount $union_mntroot || exit $?
check_not_tainted

if [ "$TEST_OVERLAYFS" == 1 ]
then
    umount $upper_mntroot || exit $?
    check_not_tainted
fi

umount $lower_mntroot || exit $?
check_not_tainted
