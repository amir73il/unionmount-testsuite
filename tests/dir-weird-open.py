#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Open of existing directory; with create, exclusive and truncate
#
###############################################################################

# Open read-only and create
echo "TEST$filenr: Open O_RDONLY | O_CREAT"
file=$testdir/dir$((filenr++))$termslash

open_file -r -c $file -E EISDIR
assert_is_upper $file
open_file -r $file
assert_is_upper $file

# Open read-only and create exclusive
echo "TEST$filenr: Open O_RDONLY | O_CREAT | O_EXCL"
file=$testdir/dir$((filenr++))$termslash

open_file -r -c -e $file -E EEXIST ${termslash:+-E EISDIR}
assert_is_upper $file
open_file -r $file
assert_is_upper $file

# Open read-only and truncate
echo "TEST$filenr: Open O_RDONLY | O_TRUNC"
file=$testdir/dir$((filenr++))$termslash

open_file -r -t $file -E EISDIR
assert_is_upper $file
open_file -r $file
assert_is_upper $file

# Open read-only and truncate create
echo "TEST$filenr: Open O_RDONLY | O_TRUNC | O_CREAT"
file=$testdir/dir$((filenr++))$termslash

open_file -r -t -c $file -E EISDIR
assert_is_upper $file
open_file -r $file
assert_is_upper $file

# Open read-only and truncate create exclusive
echo "TEST$filenr: Open O_RDONLY | O_TRUNC | O_CREAT | O_EXCL"
file=$testdir/dir$((filenr++))$termslash

open_file -r -t -c -e $file -E EEXIST ${termslash:+-E EISDIR}
assert_is_upper $file
open_file -r $file
assert_is_upper $file

# Open write-only and create
echo "TEST$filenr: Open O_RDONLY | O_CREAT"
file=$testdir/dir$((filenr++))$termslash

open_file -w -c $file -E EISDIR
assert_is_upper $file
open_file -r $file
assert_is_upper $file

# Open write-only and create exclusive
echo "TEST$filenr: Open O_RDONLY | O_CREAT | O_EXCL"
file=$testdir/dir$((filenr++))$termslash

open_file -w -c -e $file -E EEXIST ${termslash:+-E EISDIR}
assert_is_upper $file
open_file -r $file
assert_is_upper $file

# Open write-only and truncate
echo "TEST$filenr: Open O_RDONLY | O_TRUNC"
file=$testdir/dir$((filenr++))$termslash

open_file -w -t $file -E EISDIR
assert_is_upper $file
open_file -r $file
assert_is_upper $file

# Open write-only and truncate create
echo "TEST$filenr: Open O_RDONLY | O_TRUNC | O_CREAT"
file=$testdir/dir$((filenr++))$termslash

open_file -w -t -c $file -E EISDIR
assert_is_upper $file
open_file -r $file
assert_is_upper $file

# Open write-only and truncate create exclusive
echo "TEST$filenr: Open O_RDONLY | O_TRUNC | O_CREAT | O_EXCL"
file=$testdir/dir$((filenr++))$termslash

open_file -w -t -c -e $file -E EEXIST ${termslash:+-E EISDIR}
assert_is_upper $file
open_file -r $file
assert_is_upper $file
