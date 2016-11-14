from errno import *

###############################################################################
#
# Try to rename empty new directories
#
###############################################################################

# Rename an empty directory and rename it back again
def subtest_1(ctx):
    """Rename new empty dir and rename back"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2, d)
    ctx.rename(d2, d, err=ENOENT)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Rename an empty directory and remove old name
def subtest_2(ctx):
    """Rename new empty dir and remove old name"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, d2)
    ctx.rmdir(d, err=ENOENT)
    ctx.rename(d2, d)
    ctx.rename(d2, d, err=ENOENT)
    ctx.open_dir(d, ro=1)
    ctx.rmdir(d)
    ctx.rmdir(d, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Rename an empty directory and unlink old name
def subtest_3(ctx):
    """Rename new empty dir and unlink old name"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
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
    """Remove new empty dir and rename old name"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rmdir(d)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(d2, err=ENOENT)

# Unlink a directory and rename old name
def subtest_5(ctx):
    """Unlink new empty dir and rename old name"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.unlink(d, err=EISDIR)
    ctx.rename(d, d2)
    ctx.unlink(d, err=ENOENT)
    ctx.rmdir(d2)

# Rename an empty directory twice
def subtest_6(ctx):
    """Rename new empty dir twice"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()
    d3 = ctx.no_dir() + "x" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2, d3)
    ctx.rename(d2, d3, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d3, ro=1)

# Rename an empty directory over another
def subtest_7(ctx):
    """Rename new empty dir over another populated dir"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, d2, err=ENOTEMPTY)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1)

# Rename an empty directory over itself
def subtest_8(ctx):
    """Rename new empty dir over itself"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, d)
    ctx.open_dir(d, ro=1)

# Rename an empty directory over a file
def subtest_9(ctx):
    """Rename new empty dir over a file"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.non_empty_dir() + "/a" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, f, err=ENOTDIR)
    ctx.rename(d, f2, err=ENOTDIR)
    ctx.open_dir(d, ro=1)

# Rename an empty directory over the parent dir
def subtest_10(ctx):
    """Rename new empty dir over parent dir"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.config().testdir()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, d2, err=ENOTEMPTY)
    ctx.open_dir(d, ro=1)

# Rename an empty directory over an empty lower dir
def subtest_11(ctx):
    """Rename new empty dir over empty lower dir"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, d2)
    ctx.open_dir(d2, ro=1)

# Rename an empty directory over a populated lower dir
def subtest_12(ctx):
    """Rename new empty dir over populated lower dir"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, d2, err=ENOTEMPTY)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1)
    ctx.open_file(d2 + "/a", ro=1, err=ENOENT)

# Rename an empty directory over a removed empty lower dir
def subtest_11(ctx):
    """Rename new empty dir over removed empty lower dir"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rmdir(d2)
    ctx.rename(d, d2)
    ctx.open_dir(d2, ro=1)

# Rename an empty directory over a removed populated lower dir
def subtest_12(ctx):
    """Rename new empty dir over removed populated lower dir"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rmtree(d2)
    ctx.rename(d, d2)
    ctx.open_file(d2 + "/a", ro=1, err=ENOENT)
    ctx.open_dir(d2 + "/pop", ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)
