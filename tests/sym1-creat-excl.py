
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open(symlink) of existing file with O_CREAT and O_EXCL
#
###############################################################################

# Open(symlink) read-only
echo "TEST$filenr: Open(symlink) O_CREAT|O_EXCL|O_RDONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -e -r $symlink -E EEXIST
open_file -r $symlink -R ":xxx:yyy:zzz"

# Open(symlink) write-only and overwrite
echo "TEST$filenr: Open(symlink) O_CREAT|O_EXCL|O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -e -w $symlink -E EEXIST
open_file -r $symlink -R ":xxx:yyy:zzz"

# Open(symlink) write-only and append
echo "TEST$filenr: Open(symlink) O_CREAT|O_EXCL|O_APPEND|O_WRONLY"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -e -a $symlink -E EEXIST
open_file -r $symlink -R ":xxx:yyy:zzz"

# Open(symlink) read/write and overwrite
echo "TEST$filenr: Open(symlink) O_CREAT|O_EXCL|O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -e -r -w $symlink -E EEXIST
open_file -r $symlink -R ":xxx:yyy:zzz"

# Open(symlink) read/write and append
echo "TEST$filenr: Open(symlink) O_CREAT|O_EXCL|O_APPEND|O_RDWR"
symlink=$testdir/direct_sym$((filenr))$termslash
file=$testdir/foo$((filenr++))$termslash

open_file -c -e -r -a $symlink -E EEXIST
open_file -r $symlink -R ":xxx:yyy:zzz"
