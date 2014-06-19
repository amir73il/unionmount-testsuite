from errno import *

###############################################################################
#
# Try to rename empty directories
#
###############################################################################

# Rename an empty directory and rename it back again
def subtest_1(ctx):
    """Rename empty dir and rename back"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.rename(d, d2, xerr=EXDEV)
    ctx.rename(d, d2, err=ENOENT, xerr=EXDEV)
    ctx.rename(d2, d, xerr=ENOENT)
    ctx.rename(d2, d, err=ENOENT)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Rename an empty directory and remove old name
def subtest_2(ctx):
    """Rename empty dir and remove old name"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.rename(d, d2, xerr=EXDEV)
    ctx.rmdir(d, err=ENOENT, xerr=None)
    ctx.rename(d2, d, xerr=ENOENT)
    ctx.rename(d2, d, err=ENOENT)
    ctx.open_dir(d, ro=1, xerr=ENOENT)
    ctx.rmdir(d, xerr=ENOENT)
    ctx.rmdir(d, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Rename an empty directory and unlink old name
def subtest_3(ctx):
    """Rename empty dir and unlink old name"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.rename(d, d2, xerr=EXDEV)
    ctx.unlink(d, err=ENOENT, xerr=EISDIR)
    ctx.rename(d2, d, xerr=ENOENT)
    ctx.rename(d2, d, err=ENOENT)
    ctx.open_dir(d, ro=1)
    ctx.unlink(d, err=EISDIR)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Remove a directory and rename old name
def subtest_4(ctx):
    """Remove dir and rename old name"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.rmdir(d)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(d2, err=ENOENT)

# Unlink a directory and rename old name
def subtest_5(ctx):
    """Unlink dir and rename old name"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.unlink(d, err=EISDIR)
    ctx.rename(d, d2, xerr=EXDEV)
    ctx.unlink(d, err=ENOENT, xerr=EISDIR)
    ctx.rmdir(d2, xerr=ENOENT)

# Rename an empty directory twice
def subtest_6(ctx):
    """Rename empty dir twice"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()
    d3 = ctx.no_dir() + "x" + ctx.termslash()

    ctx.rename(d, d2, xerr=EXDEV)
    ctx.rename(d, d2, err=ENOENT, xerr=EXDEV)
    ctx.rename(d2, d3, xerr=ENOENT)
    ctx.rename(d2, d3, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT, xerr=None)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d3, ro=1, xerr=ENOENT)

# Rename an empty directory over another
def subtest_7(ctx):
    """Rename empty dir over another populated dir"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()

    ctx.rename(d, d2, err=ENOTEMPTY, xerr=EXDEV)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1)

# Rename an empty directory over itself
def subtest_8(ctx):
    """Rename empty dir over itself"""
    d = ctx.empty_dir() + ctx.termslash()

    ctx.rename(d, d)
    ctx.open_dir(d, ro=1)

# Rename an empty directory over a file
def subtest_9(ctx):
    """Rename empty dir over a file"""
    d = ctx.empty_dir() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.non_empty_dir() + "/a" + ctx.termslash()

    ctx.rename(d, f, err=ENOTDIR)
    ctx.rename(d, f2, err=ENOTDIR)
    ctx.open_dir(d, ro=1)

# Rename an empty directory over the parent dir
def subtest_10(ctx):
    """Rename empty dir over parent dir"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.config().testdir()

    ctx.rename(d, d2, err=ENOTEMPTY)
    ctx.open_dir(d, ro=1)
