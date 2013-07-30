#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Open through direct symlink of existing directory; with create, exclusive and
# truncate
#
###############################################################################

# Open(dir symlink) read-only and create
echo "TEST$filenr: Open(dir symlink) O_RDONLY | O_CREAT"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $symlink
open_file -r -c $symlink -E EISDIR
assert_is_lower $symlink
open_file -r $symlink
assert_is_lower $symlink
assert_is_upper $file

# Open(dir symlink) read-only and create exclusive
echo "TEST$filenr: Open(dir symlink) O_RDONLY | O_CREAT | O_EXCL"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $symlink
open_file -r -c -e $symlink -E EEXIST ${termslash:+-E EISDIR}
assert_is_lower $symlink
open_file -r $symlink
assert_is_lower $symlink
assert_is_upper $file

# Open(dir symlink) read-only and truncate
echo "TEST$filenr: Open(dir symlink) O_RDONLY | O_TRUNC"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $symlink
open_file -r -t $symlink -E EISDIR
assert_is_lower $symlink
open_file -r $symlink
assert_is_lower $symlink
assert_is_upper $file

# Open(dir symlink) read-only and truncate create
echo "TEST$filenr: Open(dir symlink) O_RDONLY | O_TRUNC | O_CREAT"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $symlink
open_file -r -t -c $symlink -E EISDIR
assert_is_lower $symlink
open_file -r $symlink
assert_is_lower $symlink
assert_is_upper $file

# Open(dir symlink) read-only and truncate create exclusive
echo "TEST$filenr: Open(dir symlink) O_RDONLY | O_TRUNC | O_CREAT | O_EXCL"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $symlink
open_file -r -t -c -e $symlink -E EEXIST ${termslash:+-E EISDIR}
assert_is_lower $symlink
open_file -r $symlink
assert_is_lower $symlink
assert_is_upper $file

# Open(dir symlink) write-only and create
echo "TEST$filenr: Open(dir symlink) O_WRONLY | O_CREAT"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $symlink
open_file -w -c $symlink -E EISDIR
assert_is_lower $symlink
open_file -r $symlink
assert_is_lower $symlink
assert_is_upper $file

# Open(dir symlink) write-only and create exclusive
echo "TEST$filenr: Open(dir symlink) O_WRONLY | O_CREAT | O_EXCL"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $symlink
open_file -w -c -e $symlink -E EEXIST ${termslash:+-E EISDIR}
assert_is_lower $symlink
open_file -r $symlink
assert_is_lower $symlink
assert_is_upper $file

# Open(dir symlink) write-only and truncate
echo "TEST$filenr: Open(dir symlink) O_WRONLY | O_TRUNC"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $symlink
open_file -w -t $symlink -E EISDIR
assert_is_lower $symlink
open_file -r $symlink
assert_is_lower $symlink
assert_is_upper $file

# Open(dir symlink) write-only and truncate create
echo "TEST$filenr: Open(dir symlink) O_WRONLY | O_TRUNC | O_CREAT"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $symlink
open_file -w -t -c $symlink -E EISDIR
assert_is_lower $symlink
open_file -r $symlink
assert_is_lower $symlink
assert_is_upper $file

# Open(dir symlink) write-only and truncate create exclusive
echo "TEST$filenr: Open(dir symlink) O_WRONLY | O_TRUNC | O_CREAT | O_EXCL"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

assert_is_lower $symlink
open_file -w -t -c -e $symlink -E EEXIST ${termslash:+-E EISDIR}
assert_is_lower $symlink
open_file -r $symlink
assert_is_lower $symlink
assert_is_upper $file
