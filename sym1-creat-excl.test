#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Open(symlink) of existing file with O_CREAT and O_EXCL
#
###############################################################################

# Open(symlink) read-only
echo "TEST$filenr: Open(symlink) O_CREAT|O_EXCL|O_RDONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $symlink
assert_is_lower $file
open_file -c -e -r $symlink -E EEXIST
assert_is_lower $symlink
open_file -r $symlink -R ":xxx:yyy:zzz"
assert_is_lower $file

# Open(symlink) write-only and overwrite
echo "TEST$filenr: Open(symlink) O_CREAT|O_EXCL|O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $symlink
assert_is_lower $file
open_file -c -e -w $symlink -E EEXIST
assert_is_lower $symlink
open_file -r $symlink -R ":xxx:yyy:zzz"
assert_is_lower $file

# Open(symlink) write-only and append
echo "TEST$filenr: Open(symlink) O_CREAT|O_EXCL|O_APPEND|O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $symlink
assert_is_lower $file
open_file -c -e -a $symlink -E EEXIST
assert_is_lower $symlink
open_file -r $symlink -R ":xxx:yyy:zzz"
assert_is_lower $file

# Open(symlink) read/write and overwrite
echo "TEST$filenr: Open(symlink) O_CREAT|O_EXCL|O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $symlink
assert_is_lower $file
open_file -c -e -r -w $symlink -E EEXIST
assert_is_lower $symlink
open_file -r $symlink -R ":xxx:yyy:zzz"
assert_is_lower $file

# Open(symlink) read/write and append
echo "TEST$filenr: Open(symlink) O_CREAT|O_EXCL|O_APPEND|O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $symlink
assert_is_lower $file
open_file -c -e -r -a $symlink -E EEXIST
assert_is_lower $symlink
open_file -r $symlink -R ":xxx:yyy:zzz"
assert_is_lower $file
