#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Attempted open of non-existent file; no special flags
#
###############################################################################

echo
echo "Try non-existent files:"

# Open read-only
echo "TEST$filenr: Open O_RDONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -r $file -E ENOENT
open_file -r $file -E ENOENT

# Open write-only and overwrite
echo "TEST$filenr: Open O_WRONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -w $file -E ENOENT
open_file -w $file -E ENOENT

# Open write-only and append
echo "TEST$filenr: Open O_APPEND|O_WRONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -a $file -E ENOENT
open_file -a $file -E ENOENT

# Open read/write and overwrite
echo "TEST$filenr: Open O_RDWR"
file=$testdir/no_foo$((filenr++))$termslash

open_file -r -w $file -E ENOENT
open_file -r -w $file -E ENOENT

# Open read/write and append
echo "TEST$filenr: Open O_APPEND|O_RDWR"
file=$testdir/no_foo$((filenr++))$termslash

open_file -r -a $file -E ENOENT
open_file -r -a $file -E ENOENT
