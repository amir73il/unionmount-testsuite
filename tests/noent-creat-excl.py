
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Creation of a not-yet existent file with O_CREAT and O_EXCL
#
###############################################################################

# Open read-only
echo "TEST$filenr: Create O_CREAT|O_EXCL|O_RDONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -e -r $file -R ""
open_file -c -e -r $file -E EEXIST
open_file -r $file -R ""

# Open write-only and overwrite
echo "TEST$filenr: Create O_CREAT|O_EXCL|O_WRONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -e -w $file -W "q"
open_file -r $file -R "q"
open_file -c -e -w $file -E EEXIST
open_file -r $file -R "q"

# Open write-only and append
echo "TEST$filenr: Create O_CREAT|O_EXCL|O_APPEND|O_WRONLY"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -e -a $file -W "q"
open_file -r $file -R "q"
open_file -c -e -a $file -E EEXIST
open_file -r $file -R "q"

# Open read/write and overwrite
echo "TEST$filenr: Create O_CREAT|O_EXCL|O_RDWR"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -e -r -w $file -W "q"
open_file -r $file -R "q"
open_file -c -e -r -w $file -E EEXIST
open_file -r $file -R "q"

# Open read/write and append
echo "TEST$filenr: Create O_CREAT|O_EXCL|O_APPEND|O_RDWR"
file=$testdir/no_foo$((filenr++))$termslash

open_file -c -e -r -a $file -W "q"
open_file -r $file -R "q"
open_file -c -e -r -a $file -E EEXIST
open_file -r $file -R "q"
