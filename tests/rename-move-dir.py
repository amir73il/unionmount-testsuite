from errno import *

###############################################################################
#
# Try to move directories
#
###############################################################################

# Move empty directory into another
def subtest_1(ctx):
    """Move empty dir into another"""
    d = ctx.empty_dir()
    n = d[d.rfind("/"):]
    d = d + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash() + n

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_dir(d, ro=1, err=ENOENT)

# Move a populated directory into another
def subtest_2(ctx):
    """Move populated dir into another"""
    d = ctx.non_empty_dir()
    n = d[d.rfind("/"):]
    d = d + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash() + n

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_file(d2 + "/a", ro=1)

# Move a populated directory into another after rename in origin dir
def subtest_3(ctx):
    """Rename populated dir and move into another"""
    d = ctx.non_empty_dir()
    n = d[d.rfind("/"):]
    d2 = d + "x" + ctx.termslash()
    d = d + ctx.termslash()
    d3 = ctx.empty_dir() + ctx.termslash() + n

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2, d3)
    ctx.rename(d2, d3, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d3, ro=1)
    ctx.open_file(d3 + "/a", ro=1)

# Move a populated directory into another and rename in other dir
def subtest_4(ctx):
    """Move populated dir into another and rename"""
    d = ctx.non_empty_dir()
    n = d[d.rfind("/"):]
    d = d + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash() + n
    d3 = ctx.empty_dir() + ctx.termslash() + n + "x"

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2, d3)
    ctx.rename(d2, d3, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d3, ro=1)
    ctx.open_file(d3 + "/a", ro=1)
