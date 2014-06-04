
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open through symlink of existing file with O_TRUNC
#
###############################################################################

# Truncate and open read-only
echo "TEST$filenr: Open(symlink) O_TRUNC|O_RDONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -t -r $symlink -R ""
open_file -t -r $symlink -R ""

# Truncate, open write-only and overwrite
echo "TEST$filenr: Open(symlink) O_TRUNC|O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -t -w $symlink -W "q"
open_file -r $symlink -R "q"
open_file -t -w $symlink -W "p"
open_file -r $symlink -R "p"

# Truncate, open write-only and append
echo "TEST$filenr: Open(symlink) O_TRUNC|O_APPEND|O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -t -a $symlink -W "q"
open_file -r $symlink -R "q"
open_file -t -a $symlink -W "p"
open_file -r $symlink -R "p"

# Truncate, open read/write and overwrite
echo "TEST$filenr: Open(symlink) O_TRUNC|O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -t -r -w $symlink -W "q"
open_file -r $symlink -R "q"
open_file -t -r -w $symlink -W "p"
open_file -r $symlink -R "p"

# Truncate, open read/write and append
echo "TEST$filenr: Open(symlink) O_TRUNC|O_APPEND|O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -t -r -a $symlink -W "q"
open_file -r $symlink -R "q"
open_file -t -r -a $symlink -W "p"
open_file -r $symlink -R "p"
