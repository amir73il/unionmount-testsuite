from errno import *

###############################################################################
#
# Try to rename files
#
###############################################################################

# Rename a file and rename it back again
def subtest_1(ctx):
    """Rename file and rename back"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()

    ctx.rename(f, f2)
    ctx.rename(f, f2, err=ENOENT)
    ctx.rename(f2, f)
    ctx.rename(f2, f, err=ENOENT)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f2, ro=1, err=ENOENT)

# Rename a file and unlink old name
def subtest_2(ctx):
    """Rename file and unlink old name"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()

    ctx.rename(f, f2)
    ctx.unlink(f, err=ENOENT)
    ctx.rename(f2, f)
    ctx.rename(f2, f, err=ENOENT)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.unlink(f)
    ctx.unlink(f, err=ENOENT)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.open_file(f2, ro=1, err=ENOENT)

# Rename a file and rmdir old name
def subtest_3(ctx):
    """Rename file and rmdir old name"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()

    ctx.rename(f, f2)
    ctx.rmdir(f, err=ENOENT)
    ctx.rename(f2, f)
    ctx.rename(f2, f, err=ENOENT)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.rmdir(f, err=ENOTDIR)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f2, ro=1, err=ENOENT)

# Unlink a file and rename old name
def subtest_4(ctx):
    """Unlink file and rename old name"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()

    ctx.unlink(f)
    ctx.rename(f, f2, err=ENOENT)
    ctx.unlink(f, err=ENOENT)
    ctx.unlink(f2, err=ENOENT)

# Rmdir a file and rename old name
def subtest_5(ctx):
    """Rmdir file and rename old name"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()

    ctx.rmdir(f, err=ENOTDIR)
    ctx.rename(f, f2)
    ctx.rmdir(f, err=ENOENT)
    ctx.unlink(f2)

# Rename a file twice
def subtest_6(ctx):
    """Rename file twice"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()
    f3 = ctx.no_file() + "x" + ctx.termslash()

    ctx.rename(f, f2)
    ctx.rename(f, f2, err=ENOENT)
    ctx.rename(f2, f3)
    ctx.rename(f2, f3, err=ENOENT)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.open_file(f2, ro=1, err=ENOENT)
    ctx.open_file(f3, ro=1, read=":xxx:yyy:zzz")

# Rename a file over another
def subtest_7(ctx):
    """Rename file over another"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.non_empty_dir() + "/a" + ctx.termslash()

    ctx.rename(f, f2)
    ctx.rename(f, f2, err=ENOENT)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.open_file(f2, ro=1, read=":xxx:yyy:zzz")

# Rename a file over itself
def subtest_8(ctx):
    """Rename file over itself"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.rename(f, f)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Rename a file over a directory
def subtest_9(ctx):
    """Rename file over a dir"""
    f = ctx.reg_file() + ctx.termslash()
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()

    ctx.rename(f, d, err=EISDIR)
    ctx.rename(f, d2, err=EISDIR)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Rename a file over the parent dir
def subtest_10(ctx):
    """Rename file over parent dir"""
    f = ctx.reg_file() + ctx.termslash()
    d = ctx.config().testdir()

    ctx.rename(f, d, err=ENOTEMPTY)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
