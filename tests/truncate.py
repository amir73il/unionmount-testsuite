from errno import *
from settings import *
from tool_box import *

###############################################################################
#
# Truncate files
#
###############################################################################

echo "TEST129: Prepare comparison"
cmpfile = testdir + "/foo129"
dd if=/dev/zero count=$((28-12)) bs=1 seek=12 conv=notrunc of=$cmpfile status=noxfer

# Truncate extant file
for loop in range(0, 29):
def subtest_1(ctx):
    ctx.begin_test(1, "Truncate to $loop")
    f = ctx.reg_file() + ctx.termslash()

    if not ctx.termslash():
        pre = ctx.get_file_size(f)
        if pre != 12:
            raise TestError(f + ": Initial size (" + pre + ") is not 12")

        ctx.truncate(f, loop)

        post = ctx.get_file_size(f)
        if post != loop:
            raise TestError(f + ": Truncated size (" + pre + ") is not " + loop)

        if post != 0:
            cmp -n $post $cmpfile $file
    else:
        ctx.truncate(f, loop, err=ENOTDIR)

subtests = [
    subtest_1,
]
