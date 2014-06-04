
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open of existing directory; O_DIRECTORY
#
###############################################################################

# Open read-only
echo "TEST$filenr: Open O_DIRECTORY | O_RDONLY"
file=$testdir/dir$((filenr++))$termslash

open_file -d -r $file
open_file -d -r $file

# Open write-only and overwrite
echo "TEST$filenr: Open O_DIRECTORY | O_WRONLY"
file=$testdir/dir$((filenr++))$termslash

open_file -d -w $file -E EISDIR
open_file -d -r $file
open_file -d -w $file -E EISDIR
open_file -d -r $file

# Open write-only and overwrite twice
echo "TEST$filenr: Open O_DIRECTORY | O_WRONLY * 2"
file=$testdir/dir$((filenr++))$termslash

open_file -d -w $file -E EISDIR
open_file -d -w $file -E EISDIR
open_file -d -r $file

# Open write-only and append
echo "TEST$filenr: Open O_DIRECTORY | O_APPEND|O_WRONLY"
file=$testdir/dir$((filenr++))$termslash

open_file -d -a $file -E EISDIR
open_file -d -r $file
open_file -d -a $file -E EISDIR
open_file -d -r $file

# Open read/write and overwrite
echo "TEST$filenr: Open O_DIRECTORY | O_RDWR"
file=$testdir/dir$((filenr++))$termslash

open_file -d -r -w $file -E EISDIR
open_file -d -r $file
open_file -d -r -w $file -E EISDIR
open_file -d -r $file

# Open read/write and append
echo "TEST$filenr: Open O_DIRECTORY | O_APPEND|O_RDWR"
file=$testdir/dir$((filenr++))$termslash

open_file -d -r -a $file -E EISDIR
open_file -d -r $file
open_file -d -r -a $file -E EISDIR
open_file -d -r $file
