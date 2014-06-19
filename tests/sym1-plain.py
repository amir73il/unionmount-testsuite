from errno import *

###############################################################################
#
# Open through symlink of existing file; no special flags
#
###############################################################################

# Open(symlink) read-only
def subtest_1(ctx):
    """Open(symlink) O_RDONLY"""
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(symlink, ro=1, read=":xxx:yyy:zzz")

# Open(symlink) write-only and overwrite
def subtest_2(ctx):
    """Open(symlink) O_WRONLY"""
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, wo=1, write="q")
    ctx.open_file(symlink, ro=1, read="qxxx:yyy:zzz")
    ctx.open_file(symlink, wo=1, write="p")
    ctx.open_file(symlink, ro=1, read="pxxx:yyy:zzz")

# Open(symlink) write-only and append
def subtest_3(ctx):
    """Open(symlink) O_APPEND|O_WRONLY"""
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, app=1, write="q")
    ctx.open_file(symlink, ro=1, read=":xxx:yyy:zzzq")
    ctx.open_file(symlink, app=1, write="p")
    ctx.open_file(symlink, ro=1, read=":xxx:yyy:zzzqp")

# Open(symlink) read/write and overwrite
def subtest_4(ctx):
    """Open(symlink) O_RDWR"""
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, rw=1, write="q")
    ctx.open_file(symlink, ro=1, read="qxxx:yyy:zzz")
    ctx.open_file(symlink, rw=1, write="p")
    ctx.open_file(symlink, ro=1, read="pxxx:yyy:zzz")

# Open(symlink) read/write and append
def subtest_5(ctx):
    """Open(symlink) O_APPEND|O_RDWR"""
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, app=1, write="q")
    ctx.open_file(symlink, ro=1, read=":xxx:yyy:zzzq")
    ctx.open_file(symlink, ro=1, app=1, write="p")
    ctx.open_file(symlink, ro=1, read=":xxx:yyy:zzzqp")
