from errno import *

###############################################################################
#
# Try to rename directories expecting EXDEV when REDIRECT_DIR=n
#
###############################################################################

# Rename empty directory within same parent
def subtest_1(ctx):
    """Rename empty dir within same parent"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.rename(d, d2, err=EXDEV)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d, ro=1)

# Move empty directory into another parent
def subtest_2(ctx):
    """Move empty dir into another parent"""
    d = ctx.empty_dir()
    n = d[d.rfind("/"):]
    d = d + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash() + n

    ctx.rename(d, d2, err=EXDEV)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d, ro=1)

# Rename a populated directory within same parent
def subtest_3(ctx):
    """Rename populated dir within same parent"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.rename(d, d2, err=EXDEV)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d, ro=1)
    ctx.open_file(d2 + "/a", ro=1, err=ENOENT)
    ctx.open_file(d + "/a", ro=1)

# Move a populated directory into another parent
def subtest_4(ctx):
    """Move populated dir into another parent"""
    d = ctx.non_empty_dir()
    n = d[d.rfind("/"):]
    d = d + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash() + n

    ctx.rename(d, d2, err=EXDEV)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d, ro=1)
    ctx.open_file(d2 + "/a", ro=1, err=ENOENT)
    ctx.open_file(d + "/a", ro=1)
