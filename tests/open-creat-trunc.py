from errno import *

###############################################################################
#
# Open of existing file with O_CREAT and O_TRUNC
#
###############################################################################

# Truncate and open read-only
def subtest_1(ctx):
    """Open O_CREAT|O_TRUNC|O_RDONLY"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, ro=1, crt=1, tr=1, read="")
    ctx.open_file(f, ro=1, crt=1, tr=1, read="")

# Truncate, open write-only and overwrite
def subtest_2(ctx):
    """Open O_CREAT|O_TRUNC|O_WRONLY"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, wo=1, crt=1, tr=1, write="q")
    ctx.open_file(f, ro=1, read="q")
    ctx.open_file(f, wo=1, crt=1, tr=1, write="p")
    ctx.open_file(f, ro=1, read="p")

# Truncate, open write-only and append
def subtest_3(ctx):
    """Open O_CREAT|O_TRUNC|O_APPEND|O_WRONLY"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, app=1, crt=1, tr=1, write="q")
    ctx.open_file(f, ro=1, read="q")
    ctx.open_file(f, app=1, crt=1, tr=1, write="p")
    ctx.open_file(f, ro=1, read="p")

# Truncate, open read/write and overwrite
def subtest_4(ctx):
    """Open O_CREAT|O_TRUNC|O_RDWR"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, rw=1, crt=1, tr=1, write="q")
    ctx.open_file(f, ro=1, read="q")
    ctx.open_file(f, rw=1, crt=1, tr=1, write="p")
    ctx.open_file(f, ro=1, read="p")

# Truncate, open read/write and append
def subtest_5(ctx):
    """Open O_CREAT|O_TRUNC|O_APPEND|O_RDWR"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, ro=1, app=1, crt=1, tr=1, write="q")
    ctx.open_file(f, ro=1, read="q")
    ctx.open_file(f, ro=1, app=1, crt=1, tr=1, write="p")
    ctx.open_file(f, ro=1, read="p")
