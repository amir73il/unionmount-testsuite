
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open through symlink of existing file; no special flags
#
###############################################################################

# Open(symlink) read-only
echo "TEST$filenr: Open(symlink) O_RDONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -r $symlink -R ":xxx:yyy:zzz"
open_file -r $symlink -R ":xxx:yyy:zzz"

# Open(symlink) write-only and overwrite
echo "TEST$filenr: Open(symlink) O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -w $symlink -W "q"
open_file -r $symlink -R "qxxx:yyy:zzz"
open_file -w $symlink -W "p"
open_file -r $symlink -R "pxxx:yyy:zzz"

# Open(symlink) write-only and append
echo "TEST$filenr: Open(symlink) O_APPEND|O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -a $symlink -W "q"
open_file -r $symlink -R ":xxx:yyy:zzzq"
open_file -a $symlink -W "p"
open_file -r $symlink -R ":xxx:yyy:zzzqp"

# Open(symlink) read/write and overwrite
echo "TEST$filenr: Open(symlink) O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -r -w $symlink -W "q"
open_file -r $symlink -R "qxxx:yyy:zzz"
open_file -r -w $symlink -W "p"
open_file -r $symlink -R "pxxx:yyy:zzz"

# Open(symlink) read/write and append
echo "TEST$filenr: Open(symlink) O_APPEND|O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -r -a $symlink -W "q"
open_file -r $symlink -R ":xxx:yyy:zzzq"
open_file -r -a $symlink -W "p"
open_file -r $symlink -R ":xxx:yyy:zzzqp"
