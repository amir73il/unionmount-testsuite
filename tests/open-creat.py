from errno import *

###############################################################################
#
# Open of existing file with O_CREAT
#
###############################################################################

# Open read-only
def subtest_1(ctx):
    """Open O_CREAT|O_RDONLY"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, ro=1, crt=1, read=":xxx:yyy:zzz")
    ctx.open_file(f, ro=1, crt=1, read=":xxx:yyy:zzz")

# Open write-only and overwrite
def subtest_2(ctx):
    """Open O_CREAT|O_WRONLY"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, wo=1, crt=1, write="q")
    ctx.open_file(f, ro=1, crt=1, read="qxxx:yyy:zzz")
    ctx.open_file(f, wo=1, crt=1, write="p")
    ctx.open_file(f, ro=1, crt=1, read="pxxx:yyy:zzz")

# Open write-only and append
def subtest_3(ctx):
    """Open O_CREAT|O_APPEND|O_WRONLY"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, app=1, crt=1, write="q")
    ctx.open_file(f, ro=1, crt=1, read=":xxx:yyy:zzzq")
    ctx.open_file(f, app=1, crt=1, write="p")
    ctx.open_file(f, ro=1, crt=1, read=":xxx:yyy:zzzqp")

# Open read/write and overwrite
def subtest_4(ctx):
    """Open O_CREAT|O_RDWR"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, rw=1, crt=1, write="q")
    ctx.open_file(f, ro=1, crt=1, read="qxxx:yyy:zzz")
    ctx.open_file(f, rw=1, crt=1, write="p")
    ctx.open_file(f, ro=1, crt=1, read="pxxx:yyy:zzz")

# Open read/write and append
def subtest_5(ctx):
    """Open O_CREAT|O_APPEND|O_RDWR"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, ro=1, app=1, crt=1, write="q")
    ctx.open_file(f, ro=1, crt=1, read=":xxx:yyy:zzzq")
    ctx.open_file(f, ro=1, app=1, crt=1, write="p")
    ctx.open_file(f, ro=1, crt=1, read=":xxx:yyy:zzzqp")
