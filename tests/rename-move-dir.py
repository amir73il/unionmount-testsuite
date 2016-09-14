from errno import *

###############################################################################
#
# Try to move directories
#
###############################################################################

# Move a directory into another
def subtest_1(ctx):
    """Move dir into another"""
    d = ctx.empty_dir()
    n = d[d.rfind("/"):]
    d = d + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()

    ctx.rename(d, d2 + n)
    ctx.rename(d, d2 + n, err=ENOENT)
    ctx.open_dir(d2 + n, ro=1)
    ctx.open_dir(d, ro=1, err=ENOENT)
