
from settings import *
from tool_box import *

declare -i filenr

###############################################################################
#
# Readlink tests
#
###############################################################################

echo "TEST$filenr: Readlink file"
file=$testdir/foo100$termslash

fs_op readlink $file -E EINVAL

echo "TEST$filenr: Readlink direct symlink to file"
file=$testdir/direct_sym100$termslash

fs_op readlink $file -R ../a/foo100

echo "TEST$filenr: Readlink indirect symlink to file"
file=$testdir/indirect_sym100$termslash

fs_op readlink $file -R direct_sym100

#
#
#
echo "TEST$filenr: Readlink dir"
file=$testdir/dir100$termslash

fs_op readlink $file -E EINVAL

echo "TEST$filenr: Readlink direct symlink to dir"
file=$testdir/direct_dir_sym100$termslash

fs_op readlink $file -R ../a/dir100 ${termslash:+-E EINVAL}

echo "TEST$filenr: Readlink indirect symlink to dir"
file=$testdir/indirect_dir_sym100$termslash

fs_op readlink $file -R $testdir/direct_dir_sym100 ${termslash:+-E EINVAL}

#
#
#
echo "TEST$filenr: Readlink absent file"
file=$testdir/no_foo100$termslash

fs_op readlink $file -E ENOENT

echo "TEST$filenr: Readlink broken symlink to absent file"
file=$testdir/pointless100$termslash

fs_op readlink $file -R no_foo100 ${termslash:+-E ENOENT}

echo "TEST$filenr: Readlink broken symlink"
file=$testdir/pointless101$termslash

fs_op readlink $file -R no_foo101 ${termslash:+-E ENOENT}

echo "TEST$filenr: Readlink absent file pointed to by broken symlink"
file=$testdir/no_foo101$termslash

fs_op readlink $file -E ENOENT
