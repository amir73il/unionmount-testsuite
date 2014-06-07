from errno import *
from tool_box import *

###############################################################################
#
# Open of existing file with O_CREAT and O_TRUNC
#
###############################################################################

# Truncate and open read-only
def subtest_1(ctx):
    ctx.begin_test(1, "Open O_CREAT|O_TRUNC|O_RDONLY")
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, ro=1, crt=1, tr=1, read=b"")
    ctx.open_file(f, ro=1, crt=1, tr=1, read=b"")

# Truncate, open write-only and overwrite
def subtest_2(ctx):
    ctx.begin_test(2, "Open O_CREAT|O_TRUNC|O_WRONLY")
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, wo=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")
    ctx.open_file(f, wo=1, crt=1, tr=1, write=b"p")
    ctx.open_file(f, ro=1, read=b"p")

# Truncate, open write-only and append
def subtest_3(ctx):
    ctx.begin_test(3, "Open O_CREAT|O_TRUNC|O_APPEND|O_WRONLY")
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, app=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")
    ctx.open_file(f, app=1, crt=1, tr=1, write=b"p")
    ctx.open_file(f, ro=1, read=b"p")

# Truncate, open read/write and overwrite
def subtest_4(ctx):
    ctx.begin_test(4, "Open O_CREAT|O_TRUNC|O_RDWR")
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, rw=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")
    ctx.open_file(f, rw=1, crt=1, tr=1, write=b"p")
    ctx.open_file(f, ro=1, read=b"p")

# Truncate, open read/write and append
def subtest_5(ctx):
    ctx.begin_test(5, "Open O_CREAT|O_TRUNC|O_APPEND|O_RDWR")
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, ro=1, app=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")
    ctx.open_file(f, ro=1, app=1, crt=1, tr=1, write=b"p")
    ctx.open_file(f, ro=1, read=b"p")

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
]
