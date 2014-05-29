#!/bin/bash

. ./settings.inc

#
# Check for taint (kernel warnings and oopses)
#
function check_not_tainted ()
{
    if [ "$CURRENT_TAINT" == "" ]
    then
	CURRENT_TAINT=0
    fi
    if [ `cat /proc/sys/kernel/tainted` != $CURRENT_TAINT ]
    then
	echo "*** TAINTED ***" >&2
	exit 99
    fi
}

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
    if [ "$termslash" == "" ]
    then
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
    fi
}

#
# Check that a file got copied up
#
function assert_early_copy_up ()
{
    if [ "$termslash" == "" ]
    then
	if [ ! -f $1 -a ! -L $1 ]
	then
	    echo $1: Test file not found >&2
	    exit 1
	fi

	if [ -d $1 ]
	then
	    if [ `stat -c "%D" $1` != $upper_dir_fs ]
	    then
		echo "$1: Test dir not on upper filesystem (line ${BASH_LINENO[0]})" >&2
		exit 1
	    fi
	else
	    if [ `stat -c "%D" $1` != $upper_fs ]
	    then
		echo "$1: Test file not on upper filesystem (line ${BASH_LINENO[0]})" >&2
		exit 1
	    fi
	fi
    fi
}

#
# Check that a file is on the upper filesystem
#
function assert_is_upper ()
{
    if [ "$termslash" == "" ]
    then
	if [ ! -e $1 ]
	then
	    echo $1: Test file not found >&2
	    exit 1
	fi

	if [ -d $1 ]
	then
	    if [ `stat -c "%D" $1` != $upper_dir_fs ]
	    then
		echo "$1: Test dir not on upper filesystem (line ${BASH_LINENO[0]})" >&2
		exit 1
	    fi
	else
	    if [ `stat -c "%D" $1` != $upper_fs ]
	    then
		echo "$1: Test file not on upper filesystem  (line ${BASH_LINENO[0]})" >&2
		exit 1
	    fi
	fi
    fi
}

#
# Attempt to open a file using the open_file program
#
function open_file ()
{
    add=
    if [ "$termslash" != "" ]
    then
	need_add=0
	add="-E ENOTDIR"
	crt=0
	for i in "$@"
	do
	    case "$i" in
		-c)
		    add="-E EISDIR"
		    crt=1
		    ;;
		*/foo*|*/direct_sym*|*/indirect_sym*|*/rootfile*)
		    need_add=1
		    ;;
		*/no_foo*)
		    need_add=1
		    if [ $crt = 0 ]
		    then
			add="-E ENOENT"
		    fi
		    ;;
		*/pointless*)
		    need_add=$crt
		    ;;
	    esac
	done
	if [ $need_add = 0 ]
	then
	    add=
	fi
    fi

    echo " - open_file" "$@" $add
    if $openfile "$@" $add
    then
	:
    else
	exit $?
    fi
    check_not_tainted
}

#
# As open_file(), but do it as the bin user
#
function open_file_as_bin ()
{
    add=
    if [ "$termslash" != "" ]
    then
	need_add=1
	add="-E ENOTDIR"
	for i in "$@"
	do
	    case "$i" in
		EACCES)
		    need_add=0
		    ;;
	    esac
	done
	if [ $need_add = 0 ]
	then
	    add=
	fi
    fi

    echo " - open_file_as_bin" "$@" $add
    if sudo -u bin $openfile "$@" $add
    then
	:
    else
	exit $?
    fi
    check_not_tainted
}

#
# Attempt to do something to a file using the fs_op program
#
function fs_op ()
{
    add=
    if [ "$termslash" != "" ]
    then
	add="-E ENOTDIR"
	for i in "$@"
	do
	    case "$i" in
		*/dir[0-9]*|*/direct_dir*|ENOENT)
		    add=""
		    ;;
	    esac
	done
    fi

    echo " - fs_op" "$@" $add
    if $fsop "$@" $add
    then
	:
    else
	exit $?
    fi
    check_not_tainted
}

#
# As fs_op(), but do it as the bin user
#
function fs_op_as_bin ()
{
    add=
    if [ "$termslash" != "" ]
    then
	add="-E ENOTDIR"
	for i in "$@"
	do
	    case "$i" in
		*/dir[0-9]*)
		    add=""
		    ;;
	    esac
	done
    fi

    echo " - fs_op_as_bin" "$@" $add
    if sudo -u bin $fsop "$@" $add
    then
	:
    else
	exit $?
    fi
    check_not_tainted
}
