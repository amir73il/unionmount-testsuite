#!/bin/bash

. ./tool_box.inc

declare -i filenr
filenr=100

###############################################################################
#
# Try to remove directories
#
###############################################################################

# Remove a directory that does not exist in the lower layer
echo "TEST$filenr: Remove nonexistent directory"
dir=$testdir/no_dir$((filenr++))$termslash

assert_does_not_exist $dir
fs_op rmdir $dir -E ENOENT
assert_does_not_exist $dir
fs_op rmdir $dir -E ENOENT
assert_does_not_exist $dir

# Remove a subdirectory from a dir that does not exist
echo "TEST$filenr: Remove subdir from nonexistent directory"
dir=$testdir/no_dir$((filenr++))/sub$termslash

assert_does_not_exist $dir
fs_op rmdir $dir -E ENOENT
assert_does_not_exist $dir
fs_op rmdir $dir -E ENOENT
assert_does_not_exist $dir

# Rmdir a file
echo "TEST$filenr: Remove-dir a file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr++))$termslash

assert_is_lower $dir
fs_op rmdir $dir -E ENOTDIR
assert_is_lower $dir
fs_op rmdir $dir -E ENOTDIR
assert_is_lower $dir
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Remove a subdir from a file
echo "TEST$filenr: Remove subdir from file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr++))/sub$termslash

assert_does_not_exist $dir
fs_op rmdir $dir -E ENOTDIR
assert_does_not_exist $dir
fs_op rmdir $dir -E ENOTDIR
assert_does_not_exist $dir
assert_is_lower $file
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Remove an empty lower directory
echo "TEST$filenr: Remove empty dir"
dir=$testdir/empty$((filenr++))$termslash
subdir=$dir/sub$termslash

assert_is_upper $dir
fs_op rmdir $dir
assert_does_not_exist $dir
fs_op rmdir $dir -E ENOENT
assert_does_not_exist $dir
fs_op rmdir $subdir -E ENOENT
assert_does_not_exist $dir
assert_does_not_exist $subdir

# Remove a non-existent directory from an empty lower directory
echo "TEST$filenr: Remove directory from empty dir"
dir=$testdir/empty$((filenr++))/sub$termslash

assert_does_not_exist $dir
fs_op rmdir $dir -E ENOENT
assert_does_not_exist $dir
fs_op rmdir $dir -E ENOENT
assert_does_not_exist $dir

# Remove a populated lower directory
echo "TEST$filenr: Remove populated directory"
dir=$testdir/dir$((filenr++))$termslash
file=$dir/a

assert_is_upper $dir
fs_op rmdir $dir -E ENOTEMPTY
assert_is_upper $dir
open_file_nt -r $file -R ""
assert_is_lower $file
fs_op unlink $file
open_file_nt -r $file -E ENOENT
fs_op unlink $file -E ENOENT
assert_does_not_exist $file
assert_is_upper $dir
fs_op rmdir $dir
assert_does_not_exist $dir
fs_op rmdir $dir -E ENOENT
open_file_nt -r $file -R "" -E ENOENT

# Remove a populated lower directory after creating a file in it
echo "TEST$filenr: Remove populated directory with created file"
dir=$testdir/empty$((filenr++))$termslash
file=$dir/b

assert_is_upper $dir
open_file_nt -c -e -w $file -W "abcq"
assert_is_upper $file
fs_op rmdir $dir -E ENOTEMPTY
fs_op_nt unlink $file
open_file_nt -r $file -E ENOENT
fs_op_nt unlink $file -E ENOENT
assert_is_upper $dir
fs_op rmdir $dir
assert_does_not_exist $dir
fs_op rmdir $dir -E ENOENT
open_file_nt -r $file -R "" -E ENOENT

# Remove a populated lower directory with copied-up file
echo "TEST$filenr: Remove populated directory with copied up file"
dir=$testdir/dir$((filenr++))$termslash
file=$dir/a

assert_is_upper $dir
fs_op rmdir $dir -E ENOTEMPTY
assert_is_upper $dir
open_file_nt -r $file -R ""
assert_is_lower $file
open_file_nt -w $file -W "abcd"
assert_is_upper $file
open_file_nt -r $file -R "abcd"
fs_op_nt unlink $file
open_file_nt -r $file -E ENOENT
fs_op_nt unlink $file -E ENOENT
assert_is_upper $dir
fs_op rmdir $dir
assert_does_not_exist $dir
fs_op rmdir $dir -E ENOENT
open_file_nt -r $file -R "" -E ENOENT

# Remove a populated lower directory after unlinking a file and creating a dir over it
echo "TEST$filenr: Remove populated directory with mkdir after unlink"
dir=$testdir/dir$((filenr++))$termslash
file=$dir/a

assert_is_upper $dir
fs_op rmdir $dir -E ENOTEMPTY
assert_is_upper $dir

open_file_nt -r $file -R ""
assert_is_lower $file
fs_op rmdir $dir -E ENOTEMPTY
fs_op_nt unlink $file
open_file_nt -r $file -E ENOENT
fs_op_nt unlink $file -E ENOENT

fs_op mkdir $file 0755
assert_is_upper $file
fs_op mkdir $file 0755 -E EEXIST
assert_is_upper $file
fs_op rmdir $dir -E ENOTEMPTY
assert_is_upper $file
fs_op rmdir $file
assert_does_not_exist $file
fs_op rmdir $file -E ENOENT
assert_does_not_exist $file

assert_is_upper $dir
fs_op rmdir $dir
assert_does_not_exist $dir
fs_op rmdir $dir -E ENOENT
open_file_nt -r $file -R "" -E ENOENT

exit 0









# Remove a directory in a populated lower directory
echo "TEST$filenr: Remove directory in dir"
dir=$testdir/dir$((filenr))$termslash
subdir=$testdir/dir$((filenr++))/sub$termslash

assert_does_not_exist $subdir
fs_op rmdir $subdir
assert_is_upper $subdir
fs_op rmdir $subdir -E EEXIST
assert_is_upper $subdir
open_file_nt -r $dir/a -R ""
assert_is_lower $dir/a

# Remove a directory over a symlink to a file
echo "TEST$filenr: Remove directory over sym to file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr))$termslash
sym=$testdir/direct_sym$((filenr++))$termslash

assert_is_lower $dir
assert_is_lower $sym
fs_op rmdir $sym -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
fs_op rmdir $sym -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
fs_op rmdir $dir -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Remove a directory over a symlink to a symlink to a file
echo "TEST$filenr: Remove directory over sym to sym to file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr))$termslash
sym=$testdir/direct_sym$((filenr))$termslash
isym=$testdir/indirect_sym$((filenr++))$termslash

assert_is_lower $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op rmdir $isym -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op rmdir $isym -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op rmdir $sym -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op rmdir $dir -E EEXIST
assert_is_lower $dir
assert_is_lower $sym
assert_is_lower $isym
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Remove a directory over a symlink to a dir
echo "TEST$filenr: Remove directory over sym to dir"
dir=$testdir/dir$((filenr))$termslash
sym=$testdir/direct_dir_sym$((filenr++))$termslash

assert_is_upper $dir
assert_is_lower $sym
fs_op rmdir $sym -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
fs_op rmdir $sym -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
fs_op rmdir $dir -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
open_file_nt -r $sym/a -R ""
assert_is_lower $sym/a
open_file_nt -r $dir/a -R ""
assert_is_lower $dir/a

# Remove a directory over a symlink to a symlink to a dir
echo "TEST$filenr: Remove directory over sym to sym to dir"
dir=$testdir/dir$((filenr))$termslash
sym=$testdir/direct_dir_sym$((filenr))$termslash
isym=$testdir/indirect_dir_sym$((filenr++))$termslash

assert_is_upper $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op rmdir $isym -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op rmdir $isym -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op rmdir $sym -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
assert_is_lower $isym
fs_op rmdir $dir -E EEXIST
assert_is_upper $dir
assert_is_lower $sym
assert_is_lower $isym
open_file_nt -r $isym/a -R ""
assert_is_lower $isym/a
open_file_nt -r $sym/a -R ""
assert_is_lower $sym/a
open_file_nt -r $dir/a -R ""
assert_is_lower $dir/a

# Remove a directory over a dangling symlink
echo "TEST$filenr: Remove directory over dangling sym"
dir=$testdir/no_foo$((filenr))$termslash
sym=$testdir/pointless$((filenr++))$termslash

assert_does_not_exist $dir
assert_is_lower $sym
fs_op rmdir $sym -E EEXIST
assert_does_not_exist $dir
assert_is_lower $sym
fs_op rmdir $sym -E EEXIST
assert_does_not_exist $dir
assert_is_lower $sym
