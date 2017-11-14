from errno import *

###############################################################################
#
# Try to rename hardlinked files
#
###############################################################################

def subtest_1(ctx):
    """Rename hardlinked file"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()
    f3 = ctx.no_file() + "-a" + ctx.termslash()
    f4 = ctx.reg_file() + "-a" + ctx.termslash()

    ctx.link(f, f2)
    ctx.rename(f2, f3)
    ctx.rename(f3, f2)
    ctx.rename(f, f4)

    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.open_file(f2, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f3, ro=1, err=ENOENT)
    ctx.open_file(f4, ro=1, read=":xxx:yyy:zzz")
