
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Creation of a not-yet existent file with O_CREAT|O_EXCL and O_TRUNC
#
###############################################################################

# Open read-only
echo "TEST$filenr: Create O_CREAT|O_EXCL|O_TRUNC|O_RDONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -e -t -r $file -R ""
open_file -c -e -t -r $file -E EEXIST
open_file -r $file -R ""

# Open write-only and overwrite
echo "TEST$filenr: Create O_CREAT|O_EXCL|O_TRUNC|O_WRONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -e -t -w $file -W "q"
open_file -r $file -R "q"
open_file -c -e -t -w $file -E EEXIST
open_file -r $file -R "q"

# Open write-only and append
echo "TEST$filenr: Create O_CREAT|O_EXCL|O_TRUNC|O_APPEND|O_WRONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -e -t -a $file -W "q"
open_file -r $file -R "q"
open_file -c -e -a $file -E EEXIST
open_file -r $file -R "q"

# Open read/write and overwrite
echo "TEST$filenr: Create O_CREAT|O_EXCL|O_TRUNC|O_RDWR"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -e -t -r -w $file -W "q"
open_file -r $file -R "q"
open_file -c -e -r -w $file -E EEXIST
open_file -r $file -R "q"

# Open read/write and append
echo "TEST$filenr: Create O_CREAT|O_EXCL|O_TRUNC|O_APPEND|O_RDWR"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -e -t -r -a $file -W "q"
open_file -r $file -R "q"
open_file -c -e -r -a $file -E EEXIST
open_file -r $file -R "q"
