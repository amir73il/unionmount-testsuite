
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open of existing directory; no special flags
#
###############################################################################

# Open read-only
echo "TEST$filenr: Open O_RDONLY"
file=$testdir/dir$((filenr++))$termslash

open_file -r $file
open_file -r $file

# Open write-only and overwrite
echo "TEST$filenr: Open O_WRONLY"
file=$testdir/dir$((filenr++))$termslash

open_file -w $file -E EISDIR
open_file -r $file
open_file -w $file -E EISDIR
open_file -r $file

# Open write-only and overwrite twice
echo "TEST$filenr: Open O_WRONLY * 2"
file=$testdir/dir$((filenr++))$termslash

open_file -w $file -E EISDIR
open_file -w $file -E EISDIR
open_file -r $file

# Open write-only and append
echo "TEST$filenr: Open O_APPEND|O_WRONLY"
file=$testdir/dir$((filenr++))$termslash

open_file -a $file -E EISDIR
open_file -r $file
open_file -a $file -E EISDIR
open_file -r $file

# Open read/write and overwrite
echo "TEST$filenr: Open O_RDWR"
file=$testdir/dir$((filenr++))$termslash

open_file -r -w $file -E EISDIR
open_file -r $file
open_file -r -w $file -E EISDIR
open_file -r $file

# Open read/write and append
echo "TEST$filenr: Open O_APPEND|O_RDWR"
file=$testdir/dir$((filenr++))$termslash

open_file -r -a $file -E EISDIR
open_file -r $file
open_file -r -a $file -E EISDIR
open_file -r $file
