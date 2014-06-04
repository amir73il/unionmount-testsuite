
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open of existing file; no special flags
#
###############################################################################

# Open read-only
echo "TEST$filenr: Open O_RDONLY"
file=$testdir/foo$((filenr++))$termslash

open_file -r $file -R ":xxx:yyy:zzz"
open_file -r $file -R ":xxx:yyy:zzz"

# Open write-only and overwrite
echo "TEST$filenr: Open O_WRONLY"
file=$testdir/foo$((filenr++))$termslash

open_file -w $file -W "q"
open_file -r $file -R "qxxx:yyy:zzz"
open_file -w $file -W "p"
open_file -r $file -R "pxxx:yyy:zzz"

# Open write-only and append
echo "TEST$filenr: Open O_APPEND|O_WRONLY"
file=$testdir/foo$((filenr++))$termslash

open_file -a $file -W "q"
open_file -r $file -R ":xxx:yyy:zzzq"
open_file -a $file -W "p"
open_file -r $file -R ":xxx:yyy:zzzqp"

# Open read/write and overwrite
echo "TEST$filenr: Open O_RDWR"
file=$testdir/foo$((filenr++))$termslash

open_file -r -w $file -W "q"
open_file -r $file -R "qxxx:yyy:zzz"
open_file -r -w $file -W "p"
open_file -r $file -R "pxxx:yyy:zzz"

# Open read/write and append
echo "TEST$filenr: Open O_APPEND|O_RDWR"
file=$testdir/foo$((filenr++))$termslash

open_file -r -a $file -W "q"
open_file -r $file -R ":xxx:yyy:zzzq"
open_file -r -a $file -W "p"
open_file -r $file -R ":xxx:yyy:zzzqp"
