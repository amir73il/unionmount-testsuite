#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Open through symlink of existing file with O_CREAT
#
###############################################################################

# Open(symlink) read-only
echo "TEST$filenr: Open(symlink) O_CREAT|O_RDONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $symlink
assert_is_lower $file
open_file -c -r $symlink -R ":xxx:yyy:zzz"
assert_is_lower $symlink
open_file -c -r $symlink -R ":xxx:yyy:zzz"
assert_is_lower $symlink
assert_is_lower $file

# Open(symlink) write-only and overwrite
echo "TEST$filenr: Open(symlink) O_CREAT|O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $symlink
assert_is_lower $file
open_file -c -w $symlink -W "q"
assert_is_lower $symlink
open_file -c -r $symlink -R "qxxx:yyy:zzz"
assert_is_lower $symlink
assert_is_upper $file
open_file -c -w $symlink -W "p"
assert_is_lower $symlink
assert_is_upper $file
open_file -c -r $symlink -R "pxxx:yyy:zzz"
assert_is_lower $symlink
assert_is_upper $file

# Open(symlink) write-only and append
echo "TEST$filenr: Open(symlink) O_CREAT|O_APPEND|O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $symlink
assert_is_lower $file
open_file -c -a $symlink -W "q"
assert_is_lower $symlink
assert_is_upper $file
open_file -c -r $symlink -R ":xxx:yyy:zzzq"
assert_is_lower $symlink
open_file -c -a $symlink -W "p"
assert_is_lower $symlink
assert_is_upper $file
open_file -c -r $symlink -R ":xxx:yyy:zzzqp"
assert_is_lower $symlink
assert_is_upper $file

# Open(symlink) read/write and overwrite
echo "TEST$filenr: Open(symlink) O_CREAT|O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $symlink
assert_is_lower $file
open_file -c -r -w $symlink -W "q"
assert_is_lower $symlink
assert_is_upper $file
open_file -c -r $symlink -R "qxxx:yyy:zzz"
assert_is_lower $symlink
open_file -c -r -w $symlink -W "p"
assert_is_lower $symlink
assert_is_upper $file
open_file -c -r $symlink -R "pxxx:yyy:zzz"
assert_is_lower $symlink
assert_is_upper $file

# Open(symlink) read/write and append
echo "TEST$filenr: Open(symlink) O_CREAT|O_APPEND|O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $symlink
assert_is_lower $file
open_file -c -r -a $symlink -W "q"
assert_is_lower $symlink
assert_is_upper $file
open_file -c -r $symlink -R ":xxx:yyy:zzzq"
assert_is_lower $symlink
open_file -c -r -a $symlink -W "p"
assert_is_lower $symlink
assert_is_upper $file
open_file -c -r $symlink -R ":xxx:yyy:zzzqp"
assert_is_lower $symlink
assert_is_upper $file
