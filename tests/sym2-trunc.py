#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Open through symlink of existing file with O_TRUNC
#
###############################################################################

# Truncate and open read-only
echo "TEST$filenr: Open(symlink->symlink) O_TRUNC|O_RDONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $indirect
assert_is_lower $file
open_file -t -r $indirect -R ""
assert_is_lower $indirect
assert_is_upper $file
open_file -t -r $indirect -R ""
assert_is_lower $indirect
assert_is_lower $direct
assert_is_upper $file

# Truncate, open write-only and overwrite
echo "TEST$filenr: Open(symlink->symlink) O_TRUNC|O_WRONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $indirect
assert_is_lower $file
open_file -t -w $indirect -W "q"
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect -R "q"
assert_is_lower $indirect
open_file -t -w $indirect -W "p"
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect -R "p"
assert_is_lower $indirect
assert_is_lower $direct
assert_is_upper $file

# Truncate, open write-only and append
echo "TEST$filenr: Open(symlink->symlink) O_TRUNC|O_APPEND|O_WRONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $indirect
assert_is_lower $file
open_file -t -a $indirect -W "q"
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect -R "q"
assert_is_lower $indirect
open_file -t -a $indirect -W "p"
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect -R "p"
assert_is_lower $indirect
assert_is_lower $direct
assert_is_upper $file

# Truncate, open read/write and overwrite
echo "TEST$filenr: Open(symlink->symlink) O_TRUNC|O_RDWR"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $indirect
assert_is_lower $file
open_file -t -r -w $indirect -W "q"
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect -R "q"
assert_is_lower $indirect
open_file -t -r -w $indirect -W "p"
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect -R "p"
assert_is_lower $indirect
assert_is_lower $direct
assert_is_upper $file

# Truncate, open read/write and append
echo "TEST$filenr: Open(symlink->symlink) O_TRUNC|O_APPEND|O_RDWR"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

assert_is_lower $indirect
assert_is_lower $file
open_file -t -r -a $indirect -W "q"
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect -R "q"
assert_is_lower $indirect
open_file -t -r -a $indirect -W "p"
assert_is_lower $indirect
assert_is_upper $file
open_file -r $indirect -R "p"
assert_is_lower $indirect
assert_is_lower $direct
assert_is_upper $file
