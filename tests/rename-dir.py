from errno import *

###############################################################################
#
# Try to rename populated directories
#
###############################################################################

# Rename a populated directory to sibling
def subtest_1(ctx):
    """Move populated dir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash() + "/x" + ctx.termslash()

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_file(d2 + "/a", ro=1)

# Rename a populated directory to sibling parent
def subtest_2(ctx):
    """Move populated subdir"""
    d = ctx.non_empty_dir() + ctx.termslash() + "/pop" + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash() + "/pop" + ctx.termslash()

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_file(d2 + "/b", ro=1)


