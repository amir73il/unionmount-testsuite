
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open(symlink->symlink) of existing file with O_CREAT and O_EXCL
#
###############################################################################

# Open(symlink->symlink) read-only
echo "TEST$filenr: Open(symlink->symlink) O_CREAT|O_EXCL|O_RDONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -e -r $indirect -E EEXIST
open_file -r $indirect -R ":xxx:yyy:zzz"

# Open(symlink->symlink) write-only and overwrite
echo "TEST$filenr: Open(symlink->symlink) O_CREAT|O_EXCL|O_WRONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -e -w $indirect -E EEXIST
open_file -r $indirect -R ":xxx:yyy:zzz"

# Open(symlink->symlink) write-only and append
echo "TEST$filenr: Open(symlink->symlink) O_CREAT|O_EXCL|O_APPEND|O_WRONLY"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -e -a $indirect -E EEXIST
open_file -r $indirect -R ":xxx:yyy:zzz"

# Open(symlink->symlink) read/write and overwrite
echo "TEST$filenr: Open(symlink->symlink) O_CREAT|O_EXCL|O_RDWR"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -e -r -w $indirect -E EEXIST
open_file -r $indirect -R ":xxx:yyy:zzz"

# Open(symlink->symlink) read/write and append
echo "TEST$filenr: Open(symlink->symlink) O_CREAT|O_EXCL|O_APPEND|O_RDWR"
indirect=$testdir/indirect_sym$((filenr))$termslash
direct=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -e -r -a $indirect -E EEXIST
open_file -r $indirect -R ":xxx:yyy:zzz"
