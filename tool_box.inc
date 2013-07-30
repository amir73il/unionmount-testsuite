#!/bin/bash

. ./settings.inc

#
# Utility to read the ID of a file (device number + inode number)
#
function get_id ()
{
    stat -c "%D-%i" $1
}

#
# Check that a file does not exist
#
function assert_does_not_exist ()
{
    if [ -e $1 ]
    then
	echo $1: Test file unexpectedly exists >&2
	exit 1
    fi
}

#
# Check that a file is on the lower fs
#
function assert_is_lower ()
{
    if [ ! -f $1 -a ! -L $1 ]
    then
	echo $1: Test file not found >&2
	exit 1
    fi

    if [ `stat -c "%D" $1` != $lower_fs ]
    then
	echo "$1: Test file not on lower filesystem (line ${BASH_LINENO[0]})" >&2
	exit 1
    fi
}

#
# Check that a file got copied up
#
function assert_early_copy_up ()
{
    if [ ! -f $1 -a ! -L $1 ]
    then
	echo $1: Test file not found >&2
	exit 1
    fi

    if [ `stat -c "%D" $1` != $upper_fs ]
    then
	echo "$1: Test file not on lower filesystem (line ${BASH_LINENO[0]})" >&2
	exit 1
    fi
}

#
# Check that a file is on the upper filesystem
#
function assert_is_upper ()
{
    if [ ! -e $1 ]
    then
	echo $1: Test file not found >&2
	exit 1
    fi

    if [ `stat -c "%D" $1` != $upper_fs ]
    then
	echo "$1: Test file not on upper filesystem  (line ${BASH_LINENO[0]})" >&2
	exit 1
    fi
}

#
# Attempt to open a file using the open_file program
#
function open_file ()
{
    echo " - open_file" "$@"
    if $openfile "$@"
    then
	:
    else
	exit $?
    fi
}

#
# As open_file(), but do it as the bin user
#
function open_file_as_bin ()
{
    echo " - open_file_as_bin" "$@"
    if sudo -u bin $openfile "$@"
    then
	:
    else
	exit $?
    fi
}

#
# Attempt to do something to a file using the fs_op program
#
function fs_op ()
{
    echo " - fs_op" "$@"
    if $fsop "$@"
    then
	:
    else
	exit $?
    fi
}

#
# As fs_op(), but do it as the bin user
#
function fs_op_as_bin ()
{
    echo " - fs_op_as_bin" "$@"
    if sudo -u bin $fsop "$@"
    then
	:
    else
	exit $?
    fi
}
