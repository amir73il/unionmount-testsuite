
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open through symlink of existing file with O_CREAT
#
###############################################################################

# Open(symlink->symlink) read-only
echo "TEST$filenr: Open(symlink->symlink) O_CREAT|O_RDONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -r $indirect -R ":xxx:yyy:zzz"
open_file -c -r $indirect -R ":xxx:yyy:zzz"

# Open(symlink->symlink) write-only and overwrite
echo "TEST$filenr: Open(symlink->symlink) O_CREAT|O_WRONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -w $indirect -W "q"
open_file -c -r $indirect -R "qxxx:yyy:zzz"
open_file -c -w $indirect -W "p"
open_file -c -r $indirect -R "pxxx:yyy:zzz"

# Open(symlink->symlink) write-only and append
echo "TEST$filenr: Open(symlink->symlink) O_CREAT|O_APPEND|O_WRONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -a $indirect -W "q"
open_file -c -r $indirect -R ":xxx:yyy:zzzq"
open_file -c -a $indirect -W "p"
open_file -c -r $indirect -R ":xxx:yyy:zzzqp"

# Open(symlink->symlink) read/write and overwrite
echo "TEST$filenr: Open(symlink->symlink) O_CREAT|O_RDWR"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -r -w $indirect -W "q"
open_file -c -r $indirect -R "qxxx:yyy:zzz"
open_file -c -r -w $indirect -W "p"
open_file -c -r $indirect -R "pxxx:yyy:zzz"

# Open(symlink->symlink) read/write and append
echo "TEST$filenr: Open(symlink->symlink) O_CREAT|O_APPEND|O_RDWR"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -r -a $indirect -W "q"
open_file -c -r $indirect -R ":xxx:yyy:zzzq"
open_file -c -r -a $indirect -W "p"
open_file -c -r $indirect -R ":xxx:yyy:zzzqp"
