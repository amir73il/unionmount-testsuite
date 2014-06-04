
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open through indirect symlink of existing directory; with create, exclusive
# and truncate
#
###############################################################################

# Open(dir symlink) read-only and create
echo "TEST$filenr: Open(dir symlink) O_RDONLY | O_CREAT"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -r -c $indirect -E EISDIR
open_file -r $indirect

# Open(dir symlink) read-only and create exclusive
echo "TEST$filenr: Open(dir symlink) O_RDONLY | O_CREAT | O_EXCL"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -r -c -e $indirect -E EEXIST ${termslash:+-E EISDIR}
open_file -r $indirect

# Open(dir symlink) read-only and truncate
echo "TEST$filenr: Open(dir symlink) O_RDONLY | O_TRUNC"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -r -t $indirect -E EISDIR
open_file -r $indirect

# Open(dir symlink) read-only and truncate create
echo "TEST$filenr: Open(dir symlink) O_RDONLY | O_TRUNC | O_CREAT"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -r -t -c $indirect -E EISDIR
open_file -r $indirect

# Open(dir symlink) read-only and truncate create exclusive
echo "TEST$filenr: Open(dir symlink) O_RDONLY | O_TRUNC | O_CREAT | O_EXCL"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -r -t -c -e $indirect -E EEXIST ${termslash:+-E EISDIR}
open_file -r $indirect

# Open(dir symlink) write-only and create
echo "TEST$filenr: Open(dir symlink) O_WRONLY | O_CREAT"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -w -c $indirect -E EISDIR
open_file -r $indirect

# Open(dir symlink) write-only and create exclusive
echo "TEST$filenr: Open(dir symlink) O_WRONLY | O_CREAT | O_EXCL"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -w -c -e $indirect -E EEXIST ${termslash:+-E EISDIR}
open_file -r $indirect

# Open(dir symlink) write-only and truncate
echo "TEST$filenr: Open(dir symlink) O_WRONLY | O_TRUNC"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -w -t $indirect -E EISDIR
open_file -r $indirect

# Open(dir symlink) write-only and truncate create
echo "TEST$filenr: Open(dir symlink) O_WRONLY | O_TRUNC | O_CREAT"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -w -t -c $indirect -E EISDIR
open_file -r $indirect

# Open(dir symlink) write-only and truncate create exclusive
echo "TEST$filenr: Open(dir symlink) O_WRONLY | O_TRUNC | O_CREAT | O_EXCL"
indirect=$testdir/indirect_dir_sym$((filenr))$termslash
direct=$testdir/direct_dir_sym$((filenr))$termslash
file=$testdir/dir$((filenr++))$termslash

open_file -w -t -c -e $indirect -E EEXIST ${termslash:+-E EISDIR}
open_file -r $indirect
