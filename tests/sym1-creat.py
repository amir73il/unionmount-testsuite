
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open through symlink of existing file with O_CREAT
#
###############################################################################

# Open(symlink) read-only
echo "TEST$filenr: Open(symlink) O_CREAT|O_RDONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -r $symlink -R ":xxx:yyy:zzz"
open_file -c -r $symlink -R ":xxx:yyy:zzz"

# Open(symlink) write-only and overwrite
echo "TEST$filenr: Open(symlink) O_CREAT|O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -w $symlink -W "q"
open_file -c -r $symlink -R "qxxx:yyy:zzz"
open_file -c -w $symlink -W "p"
open_file -c -r $symlink -R "pxxx:yyy:zzz"

# Open(symlink) write-only and append
echo "TEST$filenr: Open(symlink) O_CREAT|O_APPEND|O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -a $symlink -W "q"
open_file -c -r $symlink -R ":xxx:yyy:zzzq"
open_file -c -a $symlink -W "p"
open_file -c -r $symlink -R ":xxx:yyy:zzzqp"

# Open(symlink) read/write and overwrite
echo "TEST$filenr: Open(symlink) O_CREAT|O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -r -w $symlink -W "q"
open_file -c -r $symlink -R "qxxx:yyy:zzz"
open_file -c -r -w $symlink -W "p"
open_file -c -r $symlink -R "pxxx:yyy:zzz"

# Open(symlink) read/write and append
echo "TEST$filenr: Open(symlink) O_CREAT|O_APPEND|O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -r -a $symlink -W "q"
open_file -c -r $symlink -R ":xxx:yyy:zzzq"
open_file -c -r -a $symlink -W "p"
open_file -c -r $symlink -R ":xxx:yyy:zzzqp"
