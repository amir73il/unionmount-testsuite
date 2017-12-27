from errno import *

###############################################################################
#
# Try to hardlink directories
#
###############################################################################

# Hard link a directory
def subtest_1(ctx):
    """Hard link dir"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.link(d, d2, err=EPERM)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Hard link a file over a directory
def subtest_2(ctx):
    """Hard link file over dir"""
    f = ctx.reg_file() + ctx.termslash()
    d = ctx.empty_dir() + ctx.termslash()

    ctx.link(f, d, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_dir(d, ro=1)

# Hard link a directory over a directory
def subtest_3(ctx):
    """Hard link dir over dir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash()

    ctx.link(d, d2, err=EPERM)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1)

# Hard link a directory over a file
def subtest_4(ctx):
    """Hard link dir over dir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.link(d, f, err=EPERM)
    ctx.open_dir(d, ro=1)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Hard link a directory over itself
def subtest_5(ctx):
    """Hard link dir over itself"""
    d = ctx.non_empty_dir() + ctx.termslash()

    ctx.link(d, d, err=EPERM)
    ctx.open_dir(d, ro=1)

# Hard link a directory over its parent
def subtest_6(ctx):
    """Hard link dir over its parent"""
    d = ctx.non_empty_dir() + "/pop" + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash()

    ctx.link(d, d2, err=EPERM)
    ctx.open_dir(d, ro=1)
    ctx.open_dir(d2, ro=1)

# Hard link a removed directory
def subtest_7(ctx):
    """Hard link removed dir"""
    d = ctx.empty_dir() + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.rmdir(d)
    ctx.link(d, d2, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)

# Hard link a renamed directory
def subtest_8(ctx):
    """Hard link renamed dir"""
    d = ctx.empty_dir() + "/new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()
    d3 = ctx.no_dir() + "-a" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, d2)
    ctx.link(d, d3, err=ENOENT)
    ctx.link(d2, d, err=EPERM)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_dir(d3, ro=1, err=ENOENT)
