from errno import *
from tool_box import *

###############################################################################
#
# Open through symlink of existing file with O_CREAT
#
###############################################################################

# Open(symlink->symlink) read-only
def subtest_1(ctx):
    ctx.begin_test(1, "Open(symlink->symlink) O_CREAT|O_RDONLY")
    indirect = ctx.indirect_sym() + ctx.termslash()
    direct = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(indirect, ro=1, crt=1, read=b":xxx:yyy:zzz")
    ctx.open_file(indirect, ro=1, crt=1, read=b":xxx:yyy:zzz")

# Open(symlink->symlink) write-only and overwrite
def subtest_2(ctx):
    ctx.begin_test(2, "Open(symlink->symlink) O_CREAT|O_WRONLY")
    indirect = ctx.indirect_sym() + ctx.termslash()
    direct = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(indirect, wo=1, crt=1, write=b"q")
    ctx.open_file(indirect, ro=1, crt=1, read=b"qxxx:yyy:zzz")
    ctx.open_file(indirect, wo=1, crt=1, write=b"p")
    ctx.open_file(indirect, ro=1, crt=1, read=b"pxxx:yyy:zzz")

# Open(symlink->symlink) write-only and append
def subtest_3(ctx):
    ctx.begin_test(3, "Open(symlink->symlink) O_CREAT|O_APPEND|O_WRONLY")
    indirect = ctx.indirect_sym() + ctx.termslash()
    direct = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(indirect, app=1, crt=1, write=b"q")
    ctx.open_file(indirect, ro=1, crt=1, read=b":xxx:yyy:zzzq")
    ctx.open_file(indirect, app=1, crt=1, write=b"p")
    ctx.open_file(indirect, ro=1, crt=1, read=b":xxx:yyy:zzzqp")

# Open(symlink->symlink) read/write and overwrite
def subtest_4(ctx):
    ctx.begin_test(4, "Open(symlink->symlink) O_CREAT|O_RDWR")
    indirect = ctx.indirect_sym() + ctx.termslash()
    direct = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(indirect, rw=1, crt=1, write=b"q")
    ctx.open_file(indirect, ro=1, crt=1, read=b"qxxx:yyy:zzz")
    ctx.open_file(indirect, rw=1, crt=1, write=b"p")
    ctx.open_file(indirect, ro=1, crt=1, read=b"pxxx:yyy:zzz")

# Open(symlink->symlink) read/write and append
def subtest_5(ctx):
    ctx.begin_test(5, "Open(symlink->symlink) O_CREAT|O_APPEND|O_RDWR")
    indirect = ctx.indirect_sym() + ctx.termslash()
    direct = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(indirect, ro=1, app=1, crt=1, write=b"q")
    ctx.open_file(indirect, ro=1, crt=1, read=b":xxx:yyy:zzzq")
    ctx.open_file(indirect, ro=1, app=1, crt=1, write=b"p")
    ctx.open_file(indirect, ro=1, crt=1, read=b":xxx:yyy:zzzqp")

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
]
