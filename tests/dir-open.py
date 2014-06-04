from errno import *
from settings import *
from tool_box import *

###############################################################################
#
# Open of existing directory; no special flags
#
###############################################################################

# Open read-only
def subtest_1(ctx):
    ctx.begin_test(1, "Open O_RDONLY")
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, ro=1)
    ctx.open_file(f, ro=1)

# Open write-only and overwrite
def subtest_2(ctx):
    ctx.begin_test(2, "Open O_WRONLY")
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, wo=1, err=EISDIR)
    ctx.open_file(f, ro=1)
    ctx.open_file(f, wo=1, err=EISDIR)
    ctx.open_file(f, ro=1)

# Open write-only and overwrite twice
def subtest_3(ctx):
    ctx.begin_test(3, "Open O_WRONLY * 2")
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, wo=1, err=EISDIR)
    ctx.open_file(f, wo=1, err=EISDIR)
    ctx.open_file(f, ro=1)

# Open write-only and append
def subtest_4(ctx):
    ctx.begin_test(4, "Open O_APPEND|O_WRONLY")
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, app=1, err=EISDIR)
    ctx.open_file(f, ro=1)
    ctx.open_file(f, app=1, err=EISDIR)
    ctx.open_file(f, ro=1)

# Open read/write and overwrite
def subtest_5(ctx):
    ctx.begin_test(5, "Open O_RDWR")
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, rw=1, err=EISDIR)
    ctx.open_file(f, ro=1)
    ctx.open_file(f, rw=1, err=EISDIR)
    ctx.open_file(f, ro=1)

# Open read/write and append
def subtest_6(ctx):
    ctx.begin_test(6, "Open O_APPEND|O_RDWR")
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, ro=1, app=1, err=EISDIR)
    ctx.open_file(f, ro=1)
    ctx.open_file(f, ro=1, app=1, err=EISDIR)
    ctx.open_file(f, ro=1)

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
    subtest_6,
]
