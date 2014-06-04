
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open through a broken symlink
#
###############################################################################

# Open broken link read-only
echo "TEST$filenr: Open(broken) O_RDONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -r $symlink -E ENOENT
open_file -r $file -E ENOENT

# Open broken link write-only and overwrite
echo "TEST$filenr: Open(broken) O_WRONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -w $symlink -E ENOENT
open_file -r $file -E ENOENT

# Open broken link write-only and append
echo "TEST$filenr: Open(broken) O_APPEND|O_WRONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -a $symlink -E ENOENT
open_file -r $file -E ENOENT

# Open broken link read/write and overwrite
echo "TEST$filenr: Open(broken) O_RDWR"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -r -w $symlink -E ENOENT
open_file -r $file -E ENOENT

# Open broken link read/write and append
echo "TEST$filenr: Open(broken) O_APPEND|O_RDWR"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -r -a $symlink -E ENOENT
open_file -r $file -E ENOENT
