#!/bin/bash

. ./tool_box.inc

declare -i filenr

###############################################################################
#
# Readlink tests
#
###############################################################################

echo "Readlink file"
file=$testdir/foo100$termslash

assert_is_lower $file
fs_op readlink $file -E EINVAL
assert_is_lower $file

echo "Readlink direct symlink to file"
file=$testdir/direct_sym100$termslash

assert_is_lower $file
fs_op readlink $file -R ../a/foo100
assert_is_lower $file

echo "Readlink indirect symlink to file"
file=$testdir/indirect_sym100$termslash

assert_is_lower $file
fs_op readlink $file -R direct_sym100
assert_is_lower $file

#
#
#
echo "Readlink dir"
file=$testdir/dir100$termslash

fs_op readlink $file -E EINVAL
assert_is_upper $file

echo "Readlink direct symlink to dir"
file=$testdir/direct_dir_sym100$termslash

assert_is_lower $file
fs_op readlink $file -R ../a/dir100 ${termslash:+-E EINVAL}
assert_is_lower $file

echo "Readlink indirect symlink to dir"
file=$testdir/indirect_dir_sym100$termslash

assert_is_lower $file
fs_op readlink $file -R $testdir/direct_dir_sym100 ${termslash:+-E EINVAL}
assert_is_lower $file

#
#
#
echo "Readlink absent file"
file=$testdir/no_foo100$termslash

fs_op readlink $file -E ENOENT

echo "Readlink broken symlink to absent file"
file=$testdir/pointless100$termslash

assert_is_lower $file
fs_op readlink $file -R no_foo100 ${termslash:+-E ENOENT}
assert_is_lower $file

echo "Readlink broken symlink"
file=$testdir/pointless101$termslash

assert_is_lower $file
fs_op readlink $file -R no_foo101 ${termslash:+-E ENOENT}
assert_is_lower $file

echo "Readlink absent file pointed to by broken symlink"
file=$testdir/no_foo101$termslash

fs_op readlink $file -E ENOENT
