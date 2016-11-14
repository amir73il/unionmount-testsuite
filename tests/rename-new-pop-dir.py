from errno import *

###############################################################################
#
# Try to rename new populated directories
#
###############################################################################

# Rename a new populated directory and rename it back again
def subtest_1(ctx):
    """Rename new dir and rename back"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2, d)
    ctx.rename(d2, d, err=ENOENT)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Rename a new directory and remove old name
def subtest_2(ctx):
    """Rename new dir and remove old name"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rename(d, d2)
    ctx.rmdir(d, err=ENOENT)
    ctx.rename(d2, d)
    ctx.rename(d2, d, err=ENOENT)
    ctx.open_dir(d, ro=1)
    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Rename a new directory and unlink old name
def subtest_3(ctx):
    """Rename new dir and unlink old name"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
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
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.rename(d, d2)
    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(d2, err=ENOTEMPTY)

# Unlink a directory and rename old name
def subtest_5(ctx):
    """Unlink new dir and rename old name"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.unlink(d, err=EISDIR)
    ctx.rename(d, d2)
    ctx.unlink(d, err=ENOENT)
    ctx.rmdir(d2, err=ENOTEMPTY)

# Rename a new directory twice
def subtest_6(ctx):
    """Rename new dir twice"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()
    d3 = ctx.no_dir() + "x" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2, d3)
    ctx.rename(d2, d3, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d3, ro=1)

# Rename a new directory over another
def subtest_7(ctx):
    """Rename new dir over another populated dir"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rename(d, d2)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)

# Rename a new directory over itself
def subtest_8(ctx):
    """Rename new dir over itself"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rename(d, d)
    ctx.open_dir(d, ro=1)

# Rename a new directory over a file within that dir
def subtest_9(ctx):
    """Rename new dir over a child file"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.non_empty_dir() + "-new/a" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rename(d, f, err=ENOTDIR)
    ctx.rename(d, f2, err=EINVAL)
    ctx.open_dir(d, ro=1)

# Rename a new directory over a file within another dir
def subtest_10(ctx):
    """Rename new dir over a file"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    f = ctx.non_empty_dir() + "/a" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rename(d, f, err=ENOTDIR)
    ctx.open_dir(d, ro=1)

# Rename a new directory over the parent dir
def subtest_11(ctx):
    """Rename new dir over parent dir"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.config().testdir()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rename(d, d2, err=ENOTEMPTY)
    ctx.open_dir(d, ro=1)

# Rename a new directory over a unioned dir
def subtest_12(ctx):
    """Rename new dir over unioned dir"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rename(d, d2, err=ENOTEMPTY)
    ctx.open_dir(d, ro=1)

# Rename a new directory over a removed empty lower dir
def subtest_13(ctx):
    """Rename new dir over removed unioned empty dir"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.non_empty_dir() + "/pop/c" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rmdir(d2)
    ctx.rename(d, d2)
    ctx.open_dir(d2, ro=1)
    ctx.open_file(d2 + "/a", ro=1, read="aaaa")

# Rename a new directory over a removed populated lower dir
def subtest_14(ctx):
    """Rename new dir over removed unioned dir, different files"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.non_empty_dir() + "/pop" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/a", wo=1, crt=1, write="aaaa")
    ctx.rmtree(d2)
    ctx.rename(d, d2)
    ctx.open_dir(d2, ro=1)
    ctx.open_file(d2 + "/a", ro=1, read="aaaa")
    ctx.open_file(d2 + "/b", ro=1, err=ENOENT)

# Rename a new directory over a removed populated lower dir
def subtest_15(ctx):
    """Rename new dir over removed unioned dir, same files"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.non_empty_dir() + "/pop" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.open_file(d + "/b", wo=1, crt=1, write="aaaa")
    ctx.rmtree(d2)
    ctx.rename(d, d2)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_file(d2 + "/b", ro=1, read="aaaa")

# Rename a new directory over a removed populated lower dir
def subtest_16(ctx):
    """Rename new dir over removed unioned dir, different dirs"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.mkdir(d + "/pop", 0o755)
    ctx.open_file(d + "/pop/x", wo=1, crt=1, write="aaaa")
    ctx.rmtree(d2)
    ctx.rename(d, d2)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_file(d2 + "/pop/x", ro=1, read="aaaa")
    ctx.open_file(d2 + "/pop/b", ro=1, err=ENOENT)

# Rename a new directory over a removed populated lower dir
def subtest_17(ctx):
    """Rename new dir over removed unioned dir, same dirs"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.mkdir(d + "/pop", 0o755)
    ctx.open_file(d + "/pop/b", wo=1, crt=1, write="aaaa")
    ctx.rmtree(d2)
    ctx.rename(d, d2)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_file(d2 + "/pop/b", ro=1, read="aaaa")

# Rename a new directory over an unlinked populated lower dir
def subtest_18(ctx):
    """Rename new dir over unlinked unioned dir"""
    d = ctx.non_empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.mkdir(d + "/pop", 0o755)
    ctx.open_file(d + "/pop/b", wo=1, crt=1, write="aaaa")
    ctx.unlink(d2, err=EISDIR)
    ctx.rename(d, d2, err=ENOTEMPTY)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1)
    ctx.open_file(d + "/pop/b", ro=1, read="aaaa")
    ctx.open_file(d2 + "/pop/b", ro=1, read=":aaa:bbb:ccc")
