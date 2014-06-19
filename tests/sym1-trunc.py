from errno import *

###############################################################################
#
# Open through symlink of existing file with O_TRUNC
#
###############################################################################

# Truncate and open read-only
def subtest_1(ctx):
    """Open(symlink) O_TRUNC|O_RDONLY"""
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, tr=1, read="")
    ctx.open_file(symlink, ro=1, tr=1, read="")

# Truncate, open write-only and overwrite
def subtest_2(ctx):
    """Open(symlink) O_TRUNC|O_WRONLY"""
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, wo=1, tr=1, write="q")
    ctx.open_file(symlink, ro=1, read="q")
    ctx.open_file(symlink, wo=1, tr=1, write="p")
    ctx.open_file(symlink, ro=1, read="p")

# Truncate, open write-only and append
def subtest_3(ctx):
    """Open(symlink) O_TRUNC|O_APPEND|O_WRONLY"""
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, app=1, tr=1, write="q")
    ctx.open_file(symlink, ro=1, read="q")
    ctx.open_file(symlink, app=1, tr=1, write="p")
    ctx.open_file(symlink, ro=1, read="p")

# Truncate, open read/write and overwrite
def subtest_4(ctx):
    """Open(symlink) O_TRUNC|O_RDWR"""
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, rw=1, tr=1, write="q")
    ctx.open_file(symlink, ro=1, read="q")
    ctx.open_file(symlink, rw=1, tr=1, write="p")
    ctx.open_file(symlink, ro=1, read="p")

# Truncate, open read/write and append
def subtest_5(ctx):
    """Open(symlink) O_TRUNC|O_APPEND|O_RDWR"""
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, app=1, tr=1, write="q")
    ctx.open_file(symlink, ro=1, read="q")
    ctx.open_file(symlink, ro=1, app=1, tr=1, write="p")
    ctx.open_file(symlink, ro=1, read="p")
