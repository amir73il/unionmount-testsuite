
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open through a broken symlink with O_CREAT
#
###############################################################################

# Open/create through broken link read-only
echo "TEST$filenr: Open(broken) O_CREAT|O_RDONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -r $symlink -R ""
open_file -r $file -R ""

# Open/create through broken link write-only and overwrite
echo "TEST$filenr: Open(broken) O_CREAT|O_WRONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -w $symlink -W "q"
open_file -r $file -R "q"

# Open/create through broken link write-only and append
echo "TEST$filenr: Open(broken) O_CREAT|O_APPEND|O_WRONLY"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -a $symlink -W "q"
open_file -r $file -R "q"

# Open/create through broken link read/write and overwrite
echo "TEST$filenr: Open(broken) O_CREAT|O_RDWR"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -r -w $symlink -W "q"
open_file -r $file -R "q"

# Open/create through broken link read/write and append
echo "TEST$filenr: Open(broken) O_CREAT|O_APPEND|O_RDWR"
symlink=$testdir/pointless$((filenr))$termslash
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -r -a $symlink -W "q"
open_file -r $file -R "q"
