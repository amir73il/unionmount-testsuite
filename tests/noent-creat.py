
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Creation of a not-yet existent file with O_CREAT
#
###############################################################################

# Open read-only
echo "TEST$filenr: Create O_CREAT|O_RDONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -r $file -R ""
open_file -c -r $file -R ""

# Open write-only and overwrite
echo "TEST$filenr: Create O_CREAT|O_WRONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -w $file -W "q"
open_file -r $file -R "q"
open_file -c -w $file -W "p"
open_file -r $file -R "p"

# Open write-only and append
echo "TEST$filenr: Create O_CREAT|O_APPEND|O_WRONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -a $file -W "q"
open_file -r $file -R "q"
open_file -c -a $file -W "p"
open_file -r $file -R "qp"

# Open read/write and overwrite
echo "TEST$filenr: Create O_CREAT|O_RDWR"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -r -w $file -W "q"
open_file -r $file -R "q"
open_file -c -r -w $file -W "p"
open_file -r $file -R "p"

# Open read/write and append
echo "TEST$filenr: Create O_CREAT|O_APPEND|O_RDWR"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -r -a $file -W "q"
open_file -r $file -R "q"
open_file -c -r -a $file -W "p"
open_file -r $file -R "qp"
