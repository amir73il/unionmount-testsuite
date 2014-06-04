
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Try to violate permissions
#
###############################################################################
filenr=100

echo "TEST$filenr: Impermissible open O_TRUNC|O_WRONLY"
file=$testdir/rootfile$((filenr++))$termslash

open_file_as_bin -t -w $file -E EACCES
open_file_as_bin -w $file -E EACCES
open_file_as_bin -r $file -R ":xxx:yyy:zzz"
open_file -r $file -R ":xxx:yyy:zzz"
open_file -w $file -W "shark"
open_file -r $file -R "sharkyyy:zzz"
open_file_as_bin -r $file -R "sharkyyy:zzz"

echo "TEST$filenr: Impermissible open O_WRONLY"
file=$testdir/rootfile$((filenr++))$termslash

open_file_as_bin -w $file -E EACCES
open_file_as_bin -w $file -E EACCES
open_file_as_bin -r $file -R ":xxx:yyy:zzz"
open_file -r $file -R ":xxx:yyy:zzz"
open_file -w $file -W "shark"
open_file -r $file -R "sharkyyy:zzz"
open_file_as_bin -r $file -R "sharkyyy:zzz"

echo "TEST$filenr: Impermissible open O_APPEND"
file=$testdir/rootfile$((filenr++))$termslash

open_file_as_bin -a $file -E EACCES
open_file_as_bin -a $file -E EACCES
open_file_as_bin -r $file -R ":xxx:yyy:zzz"
open_file -r $file -R ":xxx:yyy:zzz"
open_file -a $file -W "shark"
open_file -r $file -R ":xxx:yyy:zzzshark"
open_file_as_bin -r $file -R ":xxx:yyy:zzzshark"

#
#
#
echo "TEST$filenr: Impermissible truncate"
file=$testdir/rootfile$((filenr++))$termslash

if [ "$termslash" = "" ]
then
    assert_is_lower $file
    size=`stat --printf %s $file`
    if [ x$size != x12 ]
    then 
	echo "$file: Initial size ($size) is not 12" >&2
	exit 1
    fi
fi
fs_op_as_bin truncate $file 4 -E EACCES
fs_op_as_bin truncate $file 4 -E EACCES
if [ "$termslash" = "" ]
then
    size=`stat --printf %s $file`
    if [ x$size != x12 ]
    then 
	echo "$file: Size ($size) is not still 12" >&2
	exit 1
    fi
fi
open_file_as_bin -r $file -R ":xxx:yyy:zzz"
open_file -r $file -R ":xxx:yyy:zzz"
fs_op truncate $file 4
if [ "$termslash" = "" ]
then
    size=`stat --printf %s $file`
    if [ x$size != x4 ]
    then 
	echo "$file: Size ($size) is not 4" >&2
	exit 1
    fi
fi
open_file -r $file -R ":xxx"
open_file_as_bin -r $file -R ":xxx"

#
#
#
echo "TEST$filenr: Impermissible utimes"
file=$testdir/rootfile$((filenr++))$termslash

if [ "$termslash" = "" ]
then
    assert_is_lower $file
    atime=`stat -c %X $file`
    mtime=`stat -c %Y $file`
fi
fs_op_as_bin utimes $file -E EACCES
fs_op_as_bin utimes $file -E EACCES
if [ "$termslash" = "" ]
then
    if [ `stat -c %X $file` != $atime ]
    then
	echo "$file: Access time unexpectedly changed" >&2
	exit 1
    fi
    if [ `stat -c %Y $file` != $mtime ]
    then
	echo "$file: Modification time unexpectedly changed" >&2
	exit 1
    fi
fi
fs_op utimes $file
if [ "$termslash" = "" ]
then
    if [ `stat -c %X $file` == $atime ]
    then
	echo "$file: Access time didn't change" >&2
	exit 1
    fi
    if [ `stat -c %Y $file` == $mtime ]
    then
	echo "$file: Modification time didn't change" >&2
	exit 1
    fi
    assert_is_upper $file
fi
open_file -r $file -R ":xxx:yyy:zzz"
