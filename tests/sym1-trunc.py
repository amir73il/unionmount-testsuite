from errno import *
from tool_box import *

###############################################################################
#
# Open through symlink of existing file with O_TRUNC
#
###############################################################################

# Truncate and open read-only
def subtest_1(ctx):
    ctx.begin_test(1, "Open(symlink) O_TRUNC|O_RDONLY")
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, tr=1, read=b"")
    ctx.open_file(symlink, ro=1, tr=1, read=b"")

# Truncate, open write-only and overwrite
def subtest_2(ctx):
    ctx.begin_test(2, "Open(symlink) O_TRUNC|O_WRONLY")
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, wo=1, tr=1, write=b"q")
    ctx.open_file(symlink, ro=1, read=b"q")
    ctx.open_file(symlink, wo=1, tr=1, write=b"p")
    ctx.open_file(symlink, ro=1, read=b"p")

# Truncate, open write-only and append
def subtest_3(ctx):
    ctx.begin_test(3, "Open(symlink) O_TRUNC|O_APPEND|O_WRONLY")
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, app=1, tr=1, write=b"q")
    ctx.open_file(symlink, ro=1, read=b"q")
    ctx.open_file(symlink, app=1, tr=1, write=b"p")
    ctx.open_file(symlink, ro=1, read=b"p")

# Truncate, open read/write and overwrite
def subtest_4(ctx):
    ctx.begin_test(4, "Open(symlink) O_TRUNC|O_RDWR")
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, rw=1, tr=1, write=b"q")
    ctx.open_file(symlink, ro=1, read=b"q")
    ctx.open_file(symlink, rw=1, tr=1, write=b"p")
    ctx.open_file(symlink, ro=1, read=b"p")

# Truncate, open read/write and append
def subtest_5(ctx):
    ctx.begin_test(5, "Open(symlink) O_TRUNC|O_APPEND|O_RDWR")
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, app=1, tr=1, write=b"q")
    ctx.open_file(symlink, ro=1, read=b"q")
    ctx.open_file(symlink, ro=1, app=1, tr=1, write=b"p")
    ctx.open_file(symlink, ro=1, read=b"p")

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
]