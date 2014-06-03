#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Open through indirect symlink of existing directory; no special flags
#
###############################################################################

# Open(dir symlink) read-only
echo "TEST$filenr: Open(dir symlink) O_RDONLY"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $indirect
open_file -r $indirect
assert_is_lower $indirect
open_file -r $indirect
assert_is_lower $indirect
assert_is_lower $direct
assert_is_upper $file

# Open(dir symlink) write-only and overwrite
echo "TEST$filenr: Open(dir symlink) O_WRONLY"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $indirect
open_file -w $indirect -E EISDIR
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect
assert_is_lower $indirect
open_file -w $indirect -E EISDIR
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect
assert_is_lower $indirect
assert_is_lower $direct
assert_is_upper $file

# Open(dir symlink) write-only and append
echo "TEST$filenr: Open(dir symlink) O_APPEND|O_WRONLY"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $indirect
open_file -a $indirect -E EISDIR
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect
assert_is_lower $indirect
open_file -a $indirect -E EISDIR
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect
assert_is_lower $indirect
assert_is_lower $direct
assert_is_upper $file

# Open(dir symlink) read/write and overwrite
echo "TEST$filenr: Open(dir symlink) O_RDWR"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $indirect
open_file -r -w $indirect -E EISDIR
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect
assert_is_lower $indirect
open_file -r -w $indirect -E EISDIR
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect
assert_is_lower $indirect
assert_is_lower $direct
assert_is_upper $file

# Open(dir symlink) read/write and append
echo "TEST$filenr: Open(dir symlink) O_APPEND|O_RDWR"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $indirect
open_file -r -a $indirect -E EISDIR
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect
assert_is_lower $indirect
open_file -r -a $indirect -E EISDIR
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect
assert_is_lower $indirect
assert_is_lower $direct
assert_is_upper $file
