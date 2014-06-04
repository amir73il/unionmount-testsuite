
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Unlink tests
#
###############################################################################

echo "TEST$filenr: Unlink file"
file=$testdir/foo$((filenr++))$termslash

fs_op unlink $file
open_file -r $file -E ENOENT

fs_op unlink $file -E ENOENT ${termslash:+-E ENOTDIR}
open_file -r $file -E ENOENT

echo "TEST$filenr: Unlink direct symlink to file"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -r $symlink -R ":xxx:yyy:zzz"
fs_op unlink $symlink
open_file -r $symlink -E ENOENT
open_file -r $file -R ":xxx:yyy:zzz"

fs_op unlink $symlink -E ENOENT ${termslash:+-E ENOTDIR}
open_file -r $symlink -E ENOENT
open_file -r $file -R ":xxx:yyy:zzz"

echo "TEST$filenr: Unlink indirect symlink to file"
indirect=$testdir/indirect_sym$((filenr))$termslash
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -r $indirect -R ":xxx:yyy:zzz"
fs_op unlink $indirect
open_file -r $indirect -E ENOENT
open_file -r $symlink -R ":xxx:yyy:zzz"
open_file -r $file -R ":xxx:yyy:zzz"

fs_op unlink $indirect -E ENOENT ${termslash:+-E ENOTDIR}
open_file -r $indirect -E ENOENT
open_file -r $symlink -R ":xxx:yyy:zzz"

#
#
#
echo "TEST$filenr: Unlink dir"
file=$testdir/dir$((filenr++))$termslash

fs_op unlink $file -E EISDIR
open_file -d -r $file

fs_op unlink $file -E EISDIR
open_file -d -r $file

echo "TEST$filenr: Unlink direct symlink to dir"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -d -r $symlink
fs_op unlink $symlink ${termslash:+-E ENOTDIR}
if [ "$termslash" = "" ]
then
    open_file -d -r $symlink -E ENOENT
else
    open_file -d -r $symlink
fi
open_file -d -r $file

fs_op unlink $symlink -E ENOENT ${termslash:+-E ENOTDIR}
if [ "$termslash" = "" ]
then
    open_file -d -r $symlink -E ENOENT
else
    open_file -d -r $symlink
fi
open_file -d -r $file

echo "TEST$filenr: Unlink indirect symlink to dir"
indirect=$testdir/indirect_dir_sym100$termslash
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -d -r $indirect
fs_op unlink $indirect ${termslash:+-E ENOTDIR}
if [ "$termslash" = "" ]
then
    open_file -d -r $indirect -E ENOENT
else
    open_file -d -r $indirect
fi
open_file -d -r $symlink
open_file -d -r $file

fs_op unlink $indirect -E ENOENT ${termslash:+-E ENOTDIR}
if [ "$termslash" = "" ]
then
    open_file -d -r $indirect -E ENOENT
else
    open_file -d -r $indirect
fi
open_file -d -r $symlink

#
#
#
echo "TEST$filenr: Unlink absent file"
file=$testdir/no_foo$((filenr))$termslash

fs_op unlink $file -E ENOENT
fs_op unlink $file -E ENOENT

echo "TEST$filenr: Unlink broken symlink to absent file"
file=$testdir/pointless$((filenr++))$termslash

fs_op unlink $file
fs_op unlink $file -E ENOENT ${termslash:+-E ENOTDIR}

echo "TEST$filenr: Unlink broken symlink"
file=$testdir/pointless$((filenr))$termslash

fs_op unlink $file
fs_op unlink $file -E ENOENT ${termslash:+-E ENOTDIR}

echo "TEST$filenr: Unlink absent file pointed to by broken symlink"
file=$testdir/no_foo$((filenr++))$termslash

fs_op unlink $file -E ENOENT
fs_op unlink $file -E ENOENT
