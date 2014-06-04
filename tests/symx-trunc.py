
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open through a broken symlink with O_TRUNC
#
###############################################################################

# Open and truncate broken link read-only
echo "TEST$filenr: Open(broken) O_TRUNC|O_RDONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -t -r $symlink -E ENOENT

# Open and truncate broken link write-only and overwrite
echo "TEST$filenr: Open(broken) O_TRUNC|O_WRONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -t -w $symlink -E ENOENT

# Open and truncate broken link write-only and append
echo "TEST$filenr: Open(broken) O_TRUNC|O_APPEND|O_WRONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -t -a $symlink -E ENOENT

# Open and truncate broken link read/write and overwrite
echo "TEST$filenr: Open(broken) O_TRUNC|O_RDWR"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -t -r -w $symlink -E ENOENT

# Open and truncate broken link read/write and append
echo "TEST$filenr: Open(broken) O_TRUNC|O_APPEND|O_RDWR"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -t -r -a $symlink -E ENOENT
