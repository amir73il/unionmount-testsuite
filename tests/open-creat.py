
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open of existing file with O_CREAT
#
###############################################################################

# Open read-only
echo "TEST$filenr: Open O_CREAT|O_RDONLY"
file=$testdir/foo$((filenr++))$termslash

open_file -c -r $file -R ":xxx:yyy:zzz"
open_file -c -r $file -R ":xxx:yyy:zzz"

# Open write-only and overwrite
echo "TEST$filenr: Open O_CREAT|O_WRONLY"
file=$testdir/foo$((filenr++))$termslash

open_file -c -w $file -W "q"
open_file -c -r $file -R "qxxx:yyy:zzz"
open_file -c -w $file -W "p"
open_file -c -r $file -R "pxxx:yyy:zzz"

# Open write-only and append
echo "TEST$filenr: Open O_CREAT|O_APPEND|O_WRONLY"
file=$testdir/foo$((filenr++))$termslash

open_file -c -a $file -W "q"
open_file -c -r $file -R ":xxx:yyy:zzzq"
open_file -c -a $file -W "p"
open_file -c -r $file -R ":xxx:yyy:zzzqp"

# Open read/write and overwrite
echo "TEST$filenr: Open O_CREAT|O_RDWR"
file=$testdir/foo$((filenr++))$termslash

open_file -c -r -w $file -W "q"
open_file -c -r $file -R "qxxx:yyy:zzz"
open_file -c -r -w $file -W "p"
open_file -c -r $file -R "pxxx:yyy:zzz"

# Open read/write and append
echo "TEST$filenr: Open O_CREAT|O_APPEND|O_RDWR"
file=$testdir/foo$((filenr++))$termslash

open_file -c -r -a $file -W "q"
open_file -c -r $file -R ":xxx:yyy:zzzq"
open_file -c -r -a $file -W "p"
open_file -c -r $file -R ":xxx:yyy:zzzqp"
