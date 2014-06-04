
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Truncate files
#
###############################################################################

echo "TEST129: Prepare comparison"
cmpfile=$testdir/foo129
dd if=/dev/zero count=$((28-12)) bs=1 seek=12 conv=notrunc of=$cmpfile status=noxfer

# Truncate extant file
for ((loop=0; loop<29; loop++)) {
    echo "TEST$filenr: Truncate to $loop"
    file=$testdir/foo$((filenr++))$termslash

    if [ "$termslash" = "" ]
    then
	assert_is_lower $file
	pre=`stat --printf %s $file`
	if [ x$pre != x12 ]
	then
	    echo "$file: Initial size ($pre) is not 12" >&2
	    exit 1
	fi

	fs_op truncate $file $loop

	assert_is_upper $file
	post=`stat --printf %s $file`
	if [ x$post != x$loop ]
	then
	    echo "$file: Truncated size ($pre) is not $loop" >&2
	    exit 1
	fi

	if [ $post -ne 0 ]
	then
	    cmp -n $post $cmpfile $file
	fi
    else
	fs_op truncate $file $loop -E ENOTDIR
    fi
}
