from errno import *

###############################################################################
#
# Open of existing file with O_CREAT, O_EXCL and O_TRUNC
#
###############################################################################

# Open read-only
def subtest_1(ctx):
    """Open O_CREAT|O_EXCL|O_TRUNC|O_RDONLY"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, ro=1, crt=1, ex=1, tr=1, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Open write-only and overwrite
def subtest_2(ctx):
    """Open O_CREAT|O_EXCL|O_TRUNC|O_WRONLY"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, wo=1, crt=1, ex=1, tr=1, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Open write-only and append
def subtest_3(ctx):
    """Open O_CREAT|O_EXCL|O_TRUNC|O_APPEND|O_WRONLY"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, app=1, crt=1, ex=1, tr=1, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Open read/write and overwrite
def subtest_4(ctx):
    """Open O_CREAT|O_EXCL|O_TRUNC|O_RDWR"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, rw=1, crt=1, ex=1, tr=1, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Open read/write and append
def subtest_5(ctx):
    """Open O_CREAT|O_EXCL|O_TRUNC|O_APPEND|O_RDWR"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, ro=1, app=1, crt=1, ex=1, tr=1, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
