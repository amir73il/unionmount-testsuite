#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Open through a broken symlink with O_CREAT|O_EXCL
#
###############################################################################

# Create broken link read-only
echo "TEST$filenr: Open(broken) O_CREAT|O_EXCL|O_RDONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

assert_is_lower $symlink
assert_does_not_exist $file
open_file -c -e -r $symlink -E EEXIST
assert_is_lower $symlink
assert_does_not_exist $file

# Open and truncate broken link write-only and overwrite
echo "TEST$filenr: Open(broken) O_CREAT|O_EXCL|O_WRONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

assert_is_lower $symlink
assert_does_not_exist $file
open_file -c -e -w $symlink -E EEXIST
assert_is_lower $symlink
assert_does_not_exist $file

# Open and truncate broken link write-only and append
echo "TEST$filenr: Open(broken) O_CREAT|O_EXCL|O_APPEND|O_WRONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

assert_is_lower $symlink
assert_does_not_exist $file
open_file -c -e -a $symlink -E EEXIST
assert_is_lower $symlink
assert_does_not_exist $file

# Open and truncate broken link read/write and overwrite
echo "TEST$filenr: Open(broken) O_CREAT|O_EXCL|O_RDWR"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

assert_is_lower $symlink
assert_does_not_exist $file
open_file -c -e -r -w $symlink -E EEXIST
assert_is_lower $symlink
assert_does_not_exist $file

# Open and truncate broken link read/write and append
echo "TEST$filenr: Open(broken) O_CREAT|O_EXCL|O_APPEND|O_RDWR"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

assert_is_lower $symlink
assert_does_not_exist $file
open_file -c -e -r -a $symlink -E EEXIST
assert_is_lower $symlink
assert_does_not_exist $file
