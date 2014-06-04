
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open through indirect symlink of existing directory; no special flags
#
###############################################################################

# Open(dir symlink) read-only
echo "TEST$filenr: Open(dir symlink) O_RDONLY"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -r $indirect
open_file -r $indirect

# Open(dir symlink) write-only and overwrite
echo "TEST$filenr: Open(dir symlink) O_WRONLY"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -w $indirect -E EISDIR
open_file -r $indirect
open_file -w $indirect -E EISDIR
open_file -r $indirect

# Open(dir symlink) write-only and append
echo "TEST$filenr: Open(dir symlink) O_APPEND|O_WRONLY"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -a $indirect -E EISDIR
open_file -r $indirect
open_file -a $indirect -E EISDIR
open_file -r $indirect

# Open(dir symlink) read/write and overwrite
echo "TEST$filenr: Open(dir symlink) O_RDWR"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -r -w $indirect -E EISDIR
open_file -r $indirect
open_file -r -w $indirect -E EISDIR
open_file -r $indirect

# Open(dir symlink) read/write and append
echo "TEST$filenr: Open(dir symlink) O_APPEND|O_RDWR"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -r -a $indirect -E EISDIR
open_file -r $indirect
open_file -r -a $indirect -E EISDIR
open_file -r $indirect
