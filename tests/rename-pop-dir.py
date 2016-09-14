from errno import *

###############################################################################
#
# Try to rename populated directories
#
###############################################################################

# Rename a populated directory and rename it back again
def subtest_1(ctx):
    """Rename dir and rename back"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2, d)
    ctx.rename(d2, d, err=ENOENT)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Rename a directory and remove old name
def subtest_2(ctx):
    """Rename dir and remove old name"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.rename(d, d2)
    ctx.rmdir(d, err=ENOENT)
    ctx.rename(d2, d)
    ctx.rename(d2, d, err=ENOENT)
    ctx.open_dir(d, ro=1)
    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Rename a directory and unlink old name
def subtest_3(ctx):
    """Rename dir and unlink old name"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.rename(d, d2)
    ctx.unlink(d, err=ENOENT)
    ctx.rename(d2, d)
    ctx.rename(d2, d, err=ENOENT)
    ctx.open_dir(d, ro=1)
    ctx.unlink(d, err=EISDIR)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Remove a directory and rename old name
def subtest_4(ctx):
    """Remove dir and rename old name"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.rename(d, d2)
    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(d2, err=ENOTEMPTY)

# Unlink a directory and rename old name
def subtest_5(ctx):
    """Unlink dir and rename old name"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.unlink(d, err=EISDIR)
    ctx.rename(d, d2)
    ctx.unlink(d, err=ENOENT)
    ctx.rmdir(d2, err=ENOTEMPTY)

# Rename a directory twice
def subtest_6(ctx):
    """Rename dir twice"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()
    d3 = ctx.no_dir() + "x" + ctx.termslash()

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2, d3)
    ctx.rename(d2, d3, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d3, ro=1)

# Rename a directory over another
def subtest_7(ctx):
    """Rename populated dir over another empty dir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash()

    ctx.rename(d, d2)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)

# Rename a directory over itself
def subtest_8(ctx):
    """Rename dir over itself"""
    d = ctx.non_empty_dir() + ctx.termslash()

    ctx.rename(d, d)
    ctx.open_dir(d, ro=1)

# Rename a directory over a file within that dir
def subtest_9(ctx):
    """Rename dir over a child file"""
    d = ctx.non_empty_dir() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.non_empty_dir() + "/a" + ctx.termslash()

    ctx.rename(d, f, err=ENOTDIR)
    ctx.rename(d, f2, err=EINVAL)
    ctx.open_dir(d, ro=1)

# Rename a directory over a file within another dir
def subtest_10(ctx):
    """Rename dir over a file"""
    d = ctx.non_empty_dir() + "/pop" + ctx.termslash()
    f = ctx.non_empty_dir() + "/a" + ctx.termslash()

    ctx.rename(d, f, err=ENOTDIR)
    ctx.open_dir(d, ro=1)

# Rename a directory over the parent dir
def subtest_11(ctx):
    """Rename dir over parent dir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = ctx.config().testdir()

    ctx.rename(d, d2, err=ENOTEMPTY)
    ctx.open_dir(d, ro=1)
