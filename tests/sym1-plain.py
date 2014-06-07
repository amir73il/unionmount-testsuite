from errno import *
from tool_box import *

###############################################################################
#
# Open through symlink of existing file; no special flags
#
###############################################################################

# Open(symlink) read-only
def subtest_1(ctx):
    ctx.begin_test(1, "Open(symlink) O_RDONLY")
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, read=b":xxx:yyy:zzz")
    ctx.open_file(symlink, ro=1, read=b":xxx:yyy:zzz")

# Open(symlink) write-only and overwrite
def subtest_2(ctx):
    ctx.begin_test(2, "Open(symlink) O_WRONLY")
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, wo=1, write=b"q")
    ctx.open_file(symlink, ro=1, read=b"qxxx:yyy:zzz")
    ctx.open_file(symlink, wo=1, write=b"p")
    ctx.open_file(symlink, ro=1, read=b"pxxx:yyy:zzz")

# Open(symlink) write-only and append
def subtest_3(ctx):
    ctx.begin_test(3, "Open(symlink) O_APPEND|O_WRONLY")
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, app=1, write=b"q")
    ctx.open_file(symlink, ro=1, read=b":xxx:yyy:zzzq")
    ctx.open_file(symlink, app=1, write=b"p")
    ctx.open_file(symlink, ro=1, read=b":xxx:yyy:zzzqp")

# Open(symlink) read/write and overwrite
def subtest_4(ctx):
    ctx.begin_test(4, "Open(symlink) O_RDWR")
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, rw=1, write=b"q")
    ctx.open_file(symlink, ro=1, read=b"qxxx:yyy:zzz")
    ctx.open_file(symlink, rw=1, write=b"p")
    ctx.open_file(symlink, ro=1, read=b"pxxx:yyy:zzz")

# Open(symlink) read/write and append
def subtest_5(ctx):
    ctx.begin_test(5, "Open(symlink) O_APPEND|O_RDWR")
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, app=1, write=b"q")
    ctx.open_file(symlink, ro=1, read=b":xxx:yyy:zzzq")
    ctx.open_file(symlink, ro=1, app=1, write=b"p")
    ctx.open_file(symlink, ro=1, read=b":xxx:yyy:zzzqp")

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
]
