#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Open of existing file with O_CREAT
#
###############################################################################

# Open read-only
echo "TEST$filenr: Open O_CREAT|O_RDONLY"
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $file
open_file -c -r $file -R ":xxx:yyy:zzz"
assert_is_lower $file
open_file -c -r $file -R ":xxx:yyy:zzz"
assert_is_lower $file

# Open write-only and overwrite
echo "TEST$filenr: Open O_CREAT|O_WRONLY"
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $file
open_file -c -w $file -W "q"
assert_is_upper $file
open_file -c -r $file -R "qxxx:yyy:zzz"
assert_is_upper $file
open_file -c -w $file -W "p"
assert_is_upper $file
open_file -c -r $file -R "pxxx:yyy:zzz"
assert_is_upper $file

# Open write-only and append
echo "TEST$filenr: Open O_CREAT|O_APPEND|O_WRONLY"
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $file
open_file -c -a $file -W "q"
assert_is_upper $file
open_file -c -r $file -R ":xxx:yyy:zzzq"
assert_is_upper $file
open_file -c -a $file -W "p"
assert_is_upper $file
open_file -c -r $file -R ":xxx:yyy:zzzqp"
assert_is_upper $file

# Open read/write and overwrite
echo "TEST$filenr: Open O_CREAT|O_RDWR"
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $file
open_file -c -r -w $file -W "q"
assert_is_upper $file
open_file -c -r $file -R "qxxx:yyy:zzz"
assert_is_upper $file
open_file -c -r -w $file -W "p"
assert_is_upper $file
open_file -c -r $file -R "pxxx:yyy:zzz"
assert_is_upper $file

# Open read/write and append
echo "TEST$filenr: Open O_CREAT|O_APPEND|O_RDWR"
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $file
open_file -c -r -a $file -W "q"
assert_is_upper $file
open_file -c -r $file -R ":xxx:yyy:zzzq"
assert_is_upper $file
open_file -c -r -a $file -W "p"
assert_is_upper $file
open_file -c -r $file -R ":xxx:yyy:zzzqp"
assert_is_upper $file
