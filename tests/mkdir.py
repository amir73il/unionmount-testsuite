
from settings import *
from tool_box import *

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

fs_op mkdir $dir 0755
fs_op mkdir $dir 0755 -E EEXIST

# Create a directory over a file
echo "TEST$filenr: Create directory over file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr++))$termslash

fs_op mkdir $dir 0755 -E EEXIST
fs_op mkdir $dir 0755 -E EEXIST
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Create a directory over an empty lower directory
echo "TEST$filenr: Create directory over empty dir"
dir=$testdir/empty$((filenr++))$termslash

fs_op mkdir $dir 0755 -E EEXIST

# Create a directory in an empty lower directory
echo "TEST$filenr: Create directory in empty dir"
dir=$testdir/empty$((filenr++))/sub$termslash

fs_op mkdir $dir 0755
fs_op mkdir $dir 0755 -E EEXIST

# Create a directory over a populated lower directory
echo "TEST$filenr: Create directory over dir"
dir=$testdir/dir$((filenr++))$termslash

fs_op mkdir $dir 0755 -E EEXIST
open_file_nt -r $dir/a -R ""

# Create a directory in a populated lower directory
echo "TEST$filenr: Create directory in dir"
dir=$testdir/dir$((filenr))$termslash
subdir=$testdir/dir$((filenr++))/sub$termslash

fs_op mkdir $subdir 0755
fs_op mkdir $subdir 0755 -E EEXIST
open_file_nt -r $dir/a -R ""

# Create a directory over a symlink to a file
echo "TEST$filenr: Create directory over sym to file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr))$termslash
sym=$testdir/direct_sym$((filenr++))$termslash

fs_op mkdir $sym 0755 -E EEXIST
fs_op mkdir $sym 0755 -E EEXIST
fs_op mkdir $dir 0755 -E EEXIST
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Create a directory over a symlink to a symlink to a file
echo "TEST$filenr: Create directory over sym to sym to file"
file=$testdir/foo$((filenr))
dir=$testdir/foo$((filenr))$termslash
sym=$testdir/direct_sym$((filenr))$termslash
isym=$testdir/indirect_sym$((filenr++))$termslash

fs_op mkdir $isym 0755 -E EEXIST
fs_op mkdir $isym 0755 -E EEXIST
fs_op mkdir $sym 0755 -E EEXIST
fs_op mkdir $dir 0755 -E EEXIST
open_file_nt -r $file -R ":xxx:yyy:zzz"

# Create a directory over a symlink to a dir
echo "TEST$filenr: Create directory over sym to dir"
dir=$testdir/dir$((filenr))$termslash
sym=$testdir/direct_dir_sym$((filenr++))$termslash

fs_op mkdir $sym 0755 -E EEXIST
fs_op mkdir $sym 0755 -E EEXIST
fs_op mkdir $dir 0755 -E EEXIST
open_file_nt -r $sym/a -R ""
open_file_nt -r $dir/a -R ""

# Create a directory over a symlink to a symlink to a dir
echo "TEST$filenr: Create directory over sym to sym to dir"
dir=$testdir/dir$((filenr))$termslash
sym=$testdir/direct_dir_sym$((filenr))$termslash
isym=$testdir/indirect_dir_sym$((filenr++))$termslash

fs_op mkdir $isym 0755 -E EEXIST
fs_op mkdir $isym 0755 -E EEXIST
fs_op mkdir $sym 0755 -E EEXIST
fs_op mkdir $dir 0755 -E EEXIST
open_file_nt -r $isym/a -R ""
open_file_nt -r $sym/a -R ""
open_file_nt -r $dir/a -R ""

# Create a directory over a dangling symlink
echo "TEST$filenr: Create directory over dangling sym"
dir=$testdir/no_foo$((filenr))$termslash
sym=$testdir/pointless$((filenr++))$termslash

fs_op mkdir $sym 0755 -E EEXIST
fs_op mkdir $sym 0755 -E EEXIST
