
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open through indirect symlink of existing file; no special flags
#
###############################################################################

# Open(symlink->symlink) read-only
echo "TEST$filenr: Open(symlink->symlink) O_RDONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -r $indirect -R ":xxx:yyy:zzz"
open_file -r $indirect -R ":xxx:yyy:zzz"

# Open(symlink->symlink) write-only and overwrite
echo "TEST$filenr: Open(symlink->symlink) O_WRONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -w $indirect -W "q"
open_file -r $indirect -R "qxxx:yyy:zzz"
open_file -w $indirect -W "p"
open_file -r $indirect -R "pxxx:yyy:zzz"

# Open(symlink->symlink) write-only and append
echo "TEST$filenr: Open(symlink->symlink) O_APPEND|O_WRONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -a $indirect -W "q"
open_file -r $indirect -R ":xxx:yyy:zzzq"
open_file -a $indirect -W "p"
open_file -r $indirect -R ":xxx:yyy:zzzqp"

# Open(symlink->symlink) read/write and overwrite
echo "TEST$filenr: Open(symlink->symlink) O_RDWR"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -r -w $indirect -W "q"
open_file -r $indirect -R "qxxx:yyy:zzz"
open_file -r -w $indirect -W "p"
open_file -r $indirect -R "pxxx:yyy:zzz"

# Open(symlink->symlink) read/write and append
echo "TEST$filenr: Open(symlink->symlink) O_APPEND|O_RDWR"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -r -a $indirect -W "q"
open_file -r $indirect -R ":xxx:yyy:zzzq"
open_file -r -a $indirect -W "p"
open_file -r $indirect -R ":xxx:yyy:zzzqp"
