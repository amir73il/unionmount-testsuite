from errno import *

###############################################################################
#
# Try to move directories
#
###############################################################################

# Move a directory into another
def subtest_1(ctx):
    """Move dir into another"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()
    n = d[d.rfind("/"):]

    ctx.rename(d, d2 + n, xerr=EXDEV)
    ctx.rename(d, d2 + n, err=ENOENT, xerr=EXDEV)
    ctx.open_dir(d2 + n, ro=1, xerr=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT, xerr=None)
