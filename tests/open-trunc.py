
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open of existing file with O_TRUNC
#
###############################################################################

# Truncate and open read-only
echo "TEST$filenr: Open O_TRUNC|O_RDONLY"
file=$testdir/foo$((filenr++))$termslash

open_file -t -r $file -R ""
open_file -t -r $file -R ""

# Truncate, open write-only and overwrite
echo "TEST$filenr: Open O_TRUNC|O_WRONLY"
file=$testdir/foo$((filenr++))$termslash

open_file -t -w $file -W "q"
open_file -r $file -R "q"
open_file -t -w $file -W "p"
open_file -r $file -R "p"

# Truncate, open write-only and append
echo "TEST$filenr: Open O_TRUNC|O_APPEND|O_WRONLY"
file=$testdir/foo$((filenr++))$termslash

open_file -t -a $file -W "q"
open_file -r $file -R "q"
open_file -t -a $file -W "p"
open_file -r $file -R "p"

# Truncate, open read/write and overwrite
echo "TEST$filenr: Open O_TRUNC|O_RDWR"
file=$testdir/foo$((filenr++))$termslash

open_file -t -r -w $file -W "q"
open_file -r $file -R "q"
open_file -t -r -w $file -W "p"
open_file -r $file -R "p"

# Truncate, open read/write and append
echo "TEST$filenr: Open O_TRUNC|O_APPEND|O_RDWR"
file=$testdir/foo$((filenr++))$termslash

open_file -t -r -a $file -W "q"
open_file -r $file -R "q"
open_file -t -r -a $file -W "p"
open_file -r $file -R "p"
