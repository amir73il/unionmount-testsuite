
from settings import *
from tool_box import *

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

fs_op rmdir $dir -E ENOENT
fs_op rmdir $dir -E ENOENT

# Remove a subdirectory from a dir that does not exist
echo "TEST$filenr: Remove subdir from nonexistent directory"
dir=$testdir/no_dir$((filenr++))/sub$termslash

fs_op rmdir $dir -E ENOENT
fs_op rmdir $dir -E ENOENT

# Rmdir a file
echo "TEST$filenr: Remove-dir a file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr++))$termslash

fs_op rmdir $dir -E ENOTDIR
fs_op rmdir $dir -E ENOTDIR
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Remove a subdir from a file
echo "TEST$filenr: Remove subdir from file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr++))/sub$termslash

fs_op rmdir $dir -E ENOTDIR
fs_op rmdir $dir -E ENOTDIR
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Remove an empty lower directory
echo "TEST$filenr: Remove empty dir"
dir=$testdir/empty$((filenr++))$termslash
subdir=$dir/sub$termslash

fs_op rmdir $dir
fs_op rmdir $dir -E ENOENT
fs_op rmdir $subdir -E ENOENT

# Remove a non-existent directory from an empty lower directory
echo "TEST$filenr: Remove directory from empty dir"
dir=$testdir/empty$((filenr++))/sub$termslash

fs_op rmdir $dir -E ENOENT
fs_op rmdir $dir -E ENOENT

# Remove a populated lower directory
echo "TEST$filenr: Remove populated directory"
dir=$testdir/dir$((filenr++))$termslash
file=$dir/a

fs_op rmdir $dir -E ENOTEMPTY
open_file_nt -r $file -R ""
fs_op unlink $file
open_file_nt -r $file -E ENOENT
fs_op unlink $file -E ENOENT
fs_op rmdir $dir
fs_op rmdir $dir -E ENOENT
open_file_nt -r $file -R "" -E ENOENT

# Remove a populated lower directory after creating a file in it
echo "TEST$filenr: Remove populated directory with created file"
dir=$testdir/empty$((filenr++))$termslash
file=$dir/b

open_file_nt -c -e -w $file -W "abcq"
fs_op rmdir $dir -E ENOTEMPTY
fs_op_nt unlink $file
open_file_nt -r $file -E ENOENT
fs_op_nt unlink $file -E ENOENT
fs_op rmdir $dir
fs_op rmdir $dir -E ENOENT
open_file_nt -r $file -R "" -E ENOENT

# Remove a populated lower directory with copied-up file
echo "TEST$filenr: Remove populated directory with copied up file"
dir=$testdir/dir$((filenr++))$termslash
file=$dir/a

fs_op rmdir $dir -E ENOTEMPTY
open_file_nt -r $file -R ""
open_file_nt -w $file -W "abcd"
open_file_nt -r $file -R "abcd"
fs_op_nt unlink $file
open_file_nt -r $file -E ENOENT
fs_op_nt unlink $file -E ENOENT
fs_op rmdir $dir
fs_op rmdir $dir -E ENOENT
open_file_nt -r $file -R "" -E ENOENT

# Remove a populated lower directory after unlinking a file and creating a dir over it
echo "TEST$filenr: Remove populated directory with mkdir after unlink"
dir=$testdir/dir$((filenr++))$termslash
file=$dir/a

fs_op rmdir $dir -E ENOTEMPTY

open_file_nt -r $file -R ""
fs_op rmdir $dir -E ENOTEMPTY
fs_op_nt unlink $file
open_file_nt -r $file -E ENOENT
fs_op_nt unlink $file -E ENOENT

fs_op mkdir $file 0755
fs_op mkdir $file 0755 -E EEXIST
fs_op rmdir $dir -E ENOTEMPTY
fs_op rmdir $file
fs_op rmdir $file -E ENOENT

fs_op rmdir $dir
fs_op rmdir $dir -E ENOENT
open_file_nt -r $file -R "" -E ENOENT

exit 0









# Remove a directory in a populated lower directory
echo "TEST$filenr: Remove directory in dir"
dir=$testdir/dir$((filenr))$termslash
subdir=$testdir/dir$((filenr++))/sub$termslash

fs_op rmdir $subdir
fs_op rmdir $subdir -E EEXIST
open_file_nt -r $dir/a -R ""

# Remove a directory over a symlink to a file
echo "TEST$filenr: Remove directory over sym to file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr))$termslash
sym=$testdir/direct_sym$((filenr++))$termslash

fs_op rmdir $sym -E EEXIST
fs_op rmdir $sym -E EEXIST
fs_op rmdir $dir -E EEXIST
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Remove a directory over a symlink to a symlink to a file
echo "TEST$filenr: Remove directory over sym to sym to file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr))$termslash
sym=$testdir/direct_sym$((filenr))$termslash
isym=$testdir/indirect_sym$((filenr++))$termslash

fs_op rmdir $isym -E EEXIST
fs_op rmdir $isym -E EEXIST
fs_op rmdir $sym -E EEXIST
fs_op rmdir $dir -E EEXIST
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Remove a directory over a symlink to a dir
echo "TEST$filenr: Remove directory over sym to dir"
dir=$testdir/dir$((filenr))$termslash
sym=$testdir/direct_dir_sym$((filenr++))$termslash

fs_op rmdir $sym -E EEXIST
fs_op rmdir $sym -E EEXIST
fs_op rmdir $dir -E EEXIST
open_file_nt -r $sym/a -R ""
open_file_nt -r $dir/a -R ""

# Remove a directory over a symlink to a symlink to a dir
echo "TEST$filenr: Remove directory over sym to sym to dir"
dir=$testdir/dir$((filenr))$termslash
sym=$testdir/direct_dir_sym$((filenr))$termslash
isym=$testdir/indirect_dir_sym$((filenr++))$termslash

fs_op rmdir $isym -E EEXIST
fs_op rmdir $isym -E EEXIST
fs_op rmdir $sym -E EEXIST
fs_op rmdir $dir -E EEXIST
open_file_nt -r $isym/a -R ""
open_file_nt -r $sym/a -R ""
open_file_nt -r $dir/a -R ""

# Remove a directory over a dangling symlink
echo "TEST$filenr: Remove directory over dangling sym"
dir=$testdir/no_foo$((filenr))$termslash
sym=$testdir/pointless$((filenr++))$termslash

fs_op rmdir $sym -E EEXIST
fs_op rmdir $sym -E EEXIST
