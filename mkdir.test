#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Try to create directories
#
###############################################################################

# Create a directory that does not exist in the lower layer
echo "TEST$filenr: Create directory"
dir=$testdir/no_dir$((filenr++))$termslash

assert_does_not_exist $dir
fs_op mkdir $dir 0755
assert_is_upper $dir
fs_op mkdir $dir 0755 -E EEXIST
assert_is_upper $dir

# Create a directory over a file
echo "TEST$filenr: Create directory over file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr++))$termslash

assert_is_lower $dir
fs_op mkdir $dir 0755 -E EEXIST
assert_is_lower $dir
fs_op mkdir $dir 0755 -E EEXIST
assert_is_lower $dir
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Create a directory over an empty lower directory
echo "TEST$filenr: Create directory over empty dir"
dir=$testdir/empty$((filenr++))$termslash

assert_is_upper $dir
fs_op mkdir $dir 0755 -E EEXIST
assert_is_upper $dir

# Create a directory in an empty lower directory
echo "TEST$filenr: Create directory in empty dir"
dir=$testdir/empty$((filenr++))/sub$termslash

assert_does_not_exist $dir
fs_op mkdir $dir 0755
assert_is_upper $dir
fs_op mkdir $dir 0755 -E EEXIST
assert_is_upper $dir

# Create a directory over a populated lower directory
echo "TEST$filenr: Create directory over dir"
dir=$testdir/dir$((filenr++))$termslash

assert_is_upper $dir
fs_op mkdir $dir 0755 -E EEXIST
assert_is_upper $dir
open_file_nt -r $dir/a -R ""
assert_is_lower $dir/a

# Create a directory in a populated lower directory
echo "TEST$filenr: Create directory in dir"
dir=$testdir/dir$((filenr))$termslash
subdir=$testdir/dir$((filenr++))/sub$termslash

assert_does_not_exist $subdir
fs_op mkdir $subdir 0755
assert_is_upper $subdir
fs_op mkdir $subdir 0755 -E EEXIST
assert_is_upper $subdir
open_file_nt -r $dir/a -R ""
assert_is_lower $dir/a

# Create a directory over a symlink to a file
echo "TEST$filenr: Create directory over sym to file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr))$termslash
sym=$testdir/direct_sym$((filenr++))$termslash

assert_is_lower $dir
assert_is_lower $sym
fs_op mkdir $sym 0755 -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
fs_op mkdir $sym 0755 -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
fs_op mkdir $dir 0755 -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Create a directory over a symlink to a symlink to a file
echo "TEST$filenr: Create directory over sym to sym to file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr))$termslash
sym=$testdir/direct_sym$((filenr))$termslash
isym=$testdir/indirect_sym$((filenr++))$termslash

assert_is_lower $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op mkdir $isym 0755 -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op mkdir $isym 0755 -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op mkdir $sym 0755 -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op mkdir $dir 0755 -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
assert_is_lower $isym
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Create a directory over a symlink to a dir
echo "TEST$filenr: Create directory over sym to dir"
dir=$testdir/dir$((filenr))$termslash
sym=$testdir/direct_dir_sym$((filenr++))$termslash

assert_is_upper $dir
assert_is_lower $sym
fs_op mkdir $sym 0755 -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
fs_op mkdir $sym 0755 -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
fs_op mkdir $dir 0755 -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
open_file_nt -r $sym/a -R ""
assert_is_lower $sym/a
open_file_nt -r $dir/a -R ""
assert_is_lower $dir/a

# Create a directory over a symlink to a symlink to a dir
echo "TEST$filenr: Create directory over sym to sym to dir"
dir=$testdir/dir$((filenr))$termslash
sym=$testdir/direct_dir_sym$((filenr))$termslash
isym=$testdir/indirect_dir_sym$((filenr++))$termslash

assert_is_upper $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op mkdir $isym 0755 -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op mkdir $isym 0755 -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op mkdir $sym 0755 -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op mkdir $dir 0755 -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
assert_is_lower $isym
open_file_nt -r $isym/a -R ""
assert_is_lower $isym/a
open_file_nt -r $sym/a -R ""
assert_is_lower $sym/a
open_file_nt -r $dir/a -R ""
assert_is_lower $dir/a

# Create a directory over a dangling symlink
echo "TEST$filenr: Create directory over dangling sym"
dir=$testdir/no_foo$((filenr))$termslash
sym=$testdir/pointless$((filenr++))$termslash

assert_does_not_exist $dir
assert_is_lower $sym
fs_op mkdir $sym 0755 -E EEXIST
assert_does_not_exist $dir
assert_is_lower $sym
fs_op mkdir $sym 0755 -E EEXIST
assert_does_not_exist $dir
assert_is_lower $sym
