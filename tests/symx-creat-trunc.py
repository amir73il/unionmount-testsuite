from errno import *
from tool_box import *

###############################################################################
#
# Open through a broken symlink with O_CREAT|O_TRUNC
#
###############################################################################

# Open and truncate broken link read-only
def subtest_1(ctx):
    ctx.begin_test(1, "Open(broken) O_CREAT|O_TRUNC|O_RDONLY")
    symlink = ctx.pointless() + ctx.termslash()
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, crt=1, tr=1, read=b"")
    ctx.open_file(f, ro=1, read=b"")

# Open and truncate broken link write-only and overwrite
def subtest_2(ctx):
    ctx.begin_test(2, "Open(broken) O_CREAT|O_TRUNC|O_WRONLY")
    symlink = ctx.pointless() + ctx.termslash()
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(symlink, wo=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")

# Open and truncate broken link write-only and append
def subtest_3(ctx):
    ctx.begin_test(3, "Open(broken) O_CREAT|O_TRUNC|O_APPEND|O_WRONLY")
    symlink = ctx.pointless() + ctx.termslash()
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(symlink, app=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")

# Open and truncate broken link read/write and overwrite
def subtest_4(ctx):
    ctx.begin_test(4, "Open(broken) O_CREAT|O_TRUNC|O_RDWR")
    symlink = ctx.pointless() + ctx.termslash()
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(symlink, rw=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")

# Open and truncate broken link read/write and append
def subtest_5(ctx):
    ctx.begin_test(5, "Open(broken) O_CREAT|O_TRUNC|O_APPEND|O_RDWR")
    symlink = ctx.pointless() + ctx.termslash()
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, app=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
]
