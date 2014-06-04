from errno import *
from settings import *
from tool_box import *

###############################################################################
#
# Attempted open of non-existent file; O_TRUNC
#
###############################################################################

# Open read-only
def subtest_1(ctx):
    ctx.begin_test(1, "Open O_TRUNC|O_RDONLY")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, ro=1, tr=1, err=ENOENT)
    ctx.open_file(f, ro=1, tr=1, err=ENOENT)

# Open write-only and overwrite
def subtest_2(ctx):
    ctx.begin_test(2, "Open O_TRUNC|O_WRONLY")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, wo=1, tr=1, err=ENOENT)
    ctx.open_file(f, wo=1, tr=1, err=ENOENT)

# Open write-only and append
def subtest_3(ctx):
    ctx.begin_test(3, "Open O_TRUNC|O_APPEND|O_WRONLY")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, app=1, tr=1, err=ENOENT)
    ctx.open_file(f, app=1, tr=1, err=ENOENT)

# Open read/write and overwrite
def subtest_4(ctx):
    ctx.begin_test(4, "Open O_TRUNC|O_RDWR")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, rw=1, tr=1, err=ENOENT)
    ctx.open_file(f, rw=1, tr=1, err=ENOENT)

# Open read/write and append
def subtest_5(ctx):
    ctx.begin_test(5, "Open O_TRUNC|O_APPEND|O_RDWR")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, ro=1, app=1, tr=1, err=ENOENT)
    ctx.open_file(f, ro=1, app=1, tr=1, err=ENOENT)

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
]
