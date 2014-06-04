
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open through direct symlink of existing directory; no special flags
#
###############################################################################

# Open(dir symlink) read-only
echo "TEST$filenr: Open(dir symlink) O_RDONLY"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -r $symlink
open_file -r $symlink

# Open(dir symlink) write-only and overwrite
echo "TEST$filenr: Open(dir symlink) O_WRONLY"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -w $symlink -E EISDIR
open_file -r $symlink
open_file -w $symlink -E EISDIR
open_file -r $symlink

# Open(dir symlink) write-only and append
echo "TEST$filenr: Open(dir symlink) O_APPEND|O_WRONLY"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -a $symlink -E EISDIR
open_file -r $symlink
open_file -a $symlink -E EISDIR
open_file -r $symlink

# Open(dir symlink) read/write and overwrite
echo "TEST$filenr: Open(dir symlink) O_RDWR"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -r -w $symlink -E EISDIR
open_file -r $symlink
open_file -r -w $symlink -E EISDIR
open_file -r $symlink

# Open(dir symlink) read/write and append
echo "TEST$filenr: Open(dir symlink) O_APPEND|O_RDWR"
symlink=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -r -a $symlink -E EISDIR
open_file -r $symlink
open_file -r -a $symlink -E EISDIR
open_file -r $symlink
