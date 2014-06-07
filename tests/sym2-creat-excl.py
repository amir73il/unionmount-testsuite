from errno import *
from tool_box import *

###############################################################################
#
# Open(symlink->symlink) of existing file with O_CREAT and O_EXCL
#
###############################################################################

# Open(symlink->symlink) read-only
def subtest_1(ctx):
    ctx.begin_test(1, "Open(symlink->symlink) O_CREAT|O_EXCL|O_RDONLY")
    indirect = ctx.indirect_sym() + ctx.termslash()
    direct = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(indirect, ro=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(indirect, ro=1, read=":xxx:yyy:zzz")

# Open(symlink->symlink) write-only and overwrite
def subtest_2(ctx):
    ctx.begin_test(2, "Open(symlink->symlink) O_CREAT|O_EXCL|O_WRONLY")
    indirect = ctx.indirect_sym() + ctx.termslash()
    direct = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(indirect, wo=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(indirect, ro=1, read=":xxx:yyy:zzz")

# Open(symlink->symlink) write-only and append
def subtest_3(ctx):
    ctx.begin_test(3, "Open(symlink->symlink) O_CREAT|O_EXCL|O_APPEND|O_WRONLY")
    indirect = ctx.indirect_sym() + ctx.termslash()
    direct = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(indirect, app=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(indirect, ro=1, read=":xxx:yyy:zzz")

# Open(symlink->symlink) read/write and overwrite
def subtest_4(ctx):
    ctx.begin_test(4, "Open(symlink->symlink) O_CREAT|O_EXCL|O_RDWR")
    indirect = ctx.indirect_sym() + ctx.termslash()
    direct = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(indirect, rw=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(indirect, ro=1, read=":xxx:yyy:zzz")

# Open(symlink->symlink) read/write and append
def subtest_5(ctx):
    ctx.begin_test(5, "Open(symlink->symlink) O_CREAT|O_EXCL|O_APPEND|O_RDWR")
    indirect = ctx.indirect_sym() + ctx.termslash()
    direct = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(indirect, ro=1, app=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(indirect, ro=1, read=":xxx:yyy:zzz")

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
]
