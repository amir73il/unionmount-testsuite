#
# This script tests the -o migrate feature of overlayfs.
#
# The test should be run as root are requires that the following
# directories exist and can be used as mount points:
# /lower (tmpfs and then squashfs), /upper (tmpfs) , /mnt (overlay).
#
# ./losetup is expeccted to be a modified version of losetup from
# https://github.com/amir73il/util-linux/commits/ovl-migrate
# that supports LOOP_CHANGE_FD and /dev/loop0 is expected to be
# not in use by the system.

LOSETUP=./losetup
LOOPDEV=/dev/loop0

PROG=$0

cleanup()
{
	# Cleanup test mounts
	umount /mnt /lower 2>/dev/null
	$LOSETUP $LOOPDEV 2> /dev/null | grep a.img && $LOSETUP -d $LOOPDEV
	umount /upper /lower 2>/dev/null
}

error()
{
	echo "$PROG: $1" 1>&2
	exit 1
}

[ -x $LOSETUP ] \
	|| error "modified version of losetup not found"

[[ $(id -u) == 0 ]] \
	|| error "test should be run as root"

cleanup
[ -d /mnt -a -d /lower -a -d /upper -a \
	-z "$(ls /mnt)$(ls /upper)$(ls /lower)" ] \
	|| error "test expects empty directories /mnt /lower /upper"

[ -z $($LOSETUP $LOOPDEV 2> /dev/null) ] \
	|| error "test expects $LOOPDEV not in use"

# Create overlayfs with upper tmpfs and lower squashfs image inside tmpfs
./run --ov --squashfs -s \
	|| error "failed to mount overlayfs"
mount |grep overlay|grep migrate \
	|| error "failed to mount overlay -o migrate"

# Migrate lower files to upper fs
numlowerfiles=$(find /lower | wc -l)
echo "$numlowerfiles lower files"

echo "migrating lower files..."
ls -lR /mnt > /dev/null \
	|| error "failed to migrate lower files"
numupperfiles=$(find /upper/0 | wc -l)
echo "$numupperfiles upper files"
[[ $numupperfiles == $numlowerfiles ]] \
	|| error "number of upper/lower files mismatch"

# Replace lower image with a sparse file of the same size
umount /lower
touch /upper/a.img
truncate -r /lower/a.img /upper/a.img
$LOSETUP -r /dev/loop0 /upper/a.img \
	|| error "failed to replace image file"

# Drop page and dentry cache
echo 3 > /proc/sys/vm/drop_caches

nummergedfiles=$((find /mnt || error "failed to list merged dir") | wc -l)
echo "$nummergedfiles merged files"
[[ $nummergedfiles == $numlowerfiles ]] \
	|| error "number of merged/lower files mismatch"

echo "overlayfs -o migrate test PASSED"
cleanup
exit 0
