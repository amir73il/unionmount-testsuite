#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Try to violate permissions
#
###############################################################################
filenr=100

echo "TEST$filenr: Impermissible open O_TRUNC|O_WRONLY"
file=$testdir/rootfile$((filenr++))$termslash

assert_is_lower $file
open_file_as_bin -t -w $file -E EACCES
assert_is_lower $file
open_file_as_bin -w $file -E EACCES
assert_is_lower $file
open_file_as_bin -r $file -R ":xxx:yyy:zzz"
assert_is_lower $file
open_file -r $file -R ":xxx:yyy:zzz"
assert_is_lower $file
open_file -w $file -W "shark"
assert_is_upper $file
open_file -r $file -R "sharkyyy:zzz"
assert_is_upper $file
open_file_as_bin -r $file -R "sharkyyy:zzz"

echo "TEST$filenr: Impermissible open O_WRONLY"
file=$testdir/rootfile$((filenr++))$termslash

assert_is_lower $file
open_file_as_bin -w $file -E EACCES
assert_is_lower $file
open_file_as_bin -w $file -E EACCES
assert_is_lower $file
open_file_as_bin -r $file -R ":xxx:yyy:zzz"
assert_is_lower $file
open_file -r $file -R ":xxx:yyy:zzz"
assert_is_lower $file
open_file -w $file -W "shark"
assert_is_upper $file
open_file -r $file -R "sharkyyy:zzz"
assert_is_upper $file
open_file_as_bin -r $file -R "sharkyyy:zzz"

echo "TEST$filenr: Impermissible open O_APPEND"
file=$testdir/rootfile$((filenr++))$termslash

assert_is_lower $file
open_file_as_bin -a $file -E EACCES
assert_is_lower $file
open_file_as_bin -a $file -E EACCES
assert_is_lower $file
open_file_as_bin -r $file -R ":xxx:yyy:zzz"
assert_is_lower $file
open_file -r $file -R ":xxx:yyy:zzz"
assert_is_lower $file
open_file -a $file -W "shark"
assert_is_upper $file
open_file -r $file -R ":xxx:yyy:zzzshark"
assert_is_upper $file
open_file_as_bin -r $file -R ":xxx:yyy:zzzshark"

#
#
#
echo "TEST$filenr: Impermissible truncate"
file=$testdir/rootfile$((filenr++))$termslash

if [ "$termslash" = "" ]
then
    assert_is_lower $file
    size=`stat --printf %s $file`
    if [ x$size != x12 ]
    then 
	echo "$file: Initial size ($size) is not 12" >&2
	exit 1
    fi
fi
fs_op_as_bin truncate $file 4 -E EACCES
assert_is_lower $file
fs_op_as_bin truncate $file 4 -E EACCES
assert_is_lower $file
if [ "$termslash" = "" ]
then
    size=`stat --printf %s $file`
    if [ x$size != x12 ]
    then 
	echo "$file: Size ($size) is not still 12" >&2
	exit 1
    fi
fi
open_file_as_bin -r $file -R ":xxx:yyy:zzz"
assert_is_lower $file
open_file -r $file -R ":xxx:yyy:zzz"
assert_is_lower $file
fs_op truncate $file 4
assert_is_upper $file
if [ "$termslash" = "" ]
then
    size=`stat --printf %s $file`
    if [ x$size != x4 ]
    then 
	echo "$file: Size ($size) is not 4" >&2
	exit 1
    fi
fi
open_file -r $file -R ":xxx"
assert_is_upper $file
open_file_as_bin -r $file -R ":xxx"

#
#
#
echo "TEST$filenr: Impermissible utimes"
file=$testdir/rootfile$((filenr++))$termslash

if [ "$termslash" = "" ]
then
    assert_is_lower $file
    atime=`stat -c %X $file`
    mtime=`stat -c %Y $file`
fi
fs_op_as_bin utimes $file -E EACCES
assert_early_copy_up $file
fs_op_as_bin utimes $file -E EACCES
assert_early_copy_up $file
if [ "$termslash" = "" ]
then
    if [ `stat -c %X $file` != $atime ]
    then
	echo "$file: Access time unexpectedly changed" >&2
	exit 1
    fi
    if [ `stat -c %Y $file` != $mtime ]
    then
	echo "$file: Modification time unexpectedly changed" >&2
	exit 1
    fi
fi
fs_op utimes $file
if [ "$termslash" = "" ]
then
    if [ `stat -c %X $file` == $atime ]
    then
	echo "$file: Access time didn't change" >&2
	exit 1
    fi
    if [ `stat -c %Y $file` == $mtime ]
    then
	echo "$file: Modification time didn't change" >&2
	exit 1
    fi
    assert_is_upper $file
fi
open_file -r $file -R ":xxx:yyy:zzz"
