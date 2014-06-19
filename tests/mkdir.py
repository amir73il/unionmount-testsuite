from errno import *

###############################################################################
#
# Try to create directories
#
###############################################################################

# Create a directory that does not exist in the lower layer
def subtest_1(ctx):
    """Create directory"""
    d = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.mkdir(d, 0o755, err=EEXIST)

# Create a directory over a file
def subtest_2(ctx):
    """Create directory over file"""
    f = ctx.reg_file()
    d = ctx.reg_file() + ctx.termslash()

    ctx.mkdir(d, 0o755, err=EEXIST)
    ctx.mkdir(d, 0o755, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Create a directory over an empty lower directory
def subtest_3(ctx):
    """Create directory over empty dir"""
    d = ctx.empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755, err=EEXIST)

# Create a directory in an empty lower directory
def subtest_4(ctx):
    """Create directory in empty dir"""
    d = ctx.empty_dir() + "/sub" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.mkdir(d, 0o755, err=EEXIST)

# Create a directory over a populated lower directory
def subtest_5(ctx):
    """Create directory over dir"""
    d = ctx.non_empty_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755, err=EEXIST)
    ctx.open_file(d + "/a", ro=1, read="")

# Create a directory in a populated lower directory
def subtest_6(ctx):
    """Create directory in dir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    subdir = ctx.non_empty_dir() + "/sub" + ctx.termslash()

    ctx.mkdir(subdir, 0o755)
    ctx.mkdir(subdir, 0o755, err=EEXIST)
    ctx.open_file(d + "/a", ro=1, read="")

# Create a directory over a symlink to a file
def subtest_7(ctx):
    """Create directory over sym to file"""
    f = ctx.reg_file()
    d = ctx.reg_file() + ctx.termslash()
    sym = ctx.direct_sym() + ctx.termslash()

    ctx.mkdir(sym, 0o755, err=EEXIST)
    ctx.mkdir(sym, 0o755, err=EEXIST)
    ctx.mkdir(d, 0o755, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Create a directory over a symlink to a symlink to a file
def subtest_8(ctx):
    """Create directory over sym to sym to file"""
    f = ctx.reg_file()
    d = ctx.reg_file() + ctx.termslash()
    sym = ctx.direct_sym() + ctx.termslash()
    isym = ctx.indirect_sym() + ctx.termslash()

    ctx.mkdir(isym, 0o755, err=EEXIST)
    ctx.mkdir(isym, 0o755, err=EEXIST)
    ctx.mkdir(sym, 0o755, err=EEXIST)
    ctx.mkdir(d, 0o755, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Create a directory over a symlink to a dir
def subtest_9(ctx):
    """Create directory over sym to dir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    sym = ctx.direct_dir_sym() + ctx.termslash()

    ctx.mkdir(sym, 0o755, err=EEXIST)
    ctx.mkdir(sym, 0o755, err=EEXIST)
    ctx.mkdir(d, 0o755, err=EEXIST)
    ctx.open_file(sym + "/a", ro=1, read="")
    ctx.open_file(d + "/a", ro=1, read="")

# Create a directory over a symlink to a symlink to a dir
def subtest_10(ctx):
    """Create directory over sym to sym to dir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    sym = ctx.direct_dir_sym() + ctx.termslash()
    isym = ctx.indirect_dir_sym() + ctx.termslash()

    ctx.mkdir(isym, 0o755, err=EEXIST)
    ctx.mkdir(isym, 0o755, err=EEXIST)
    ctx.mkdir(sym, 0o755, err=EEXIST)
    ctx.mkdir(d, 0o755, err=EEXIST)
    ctx.open_file(isym + "/a", ro=1, read="")
    ctx.open_file(sym + "/a", ro=1, read="")
    ctx.open_file(d + "/a", ro=1, read="")

# Create a directory over a dangling symlink
def subtest_11(ctx):
    """Create directory over dangling sym"""
    d = ctx.no_file() + ctx.termslash()
    sym = ctx.pointless() + ctx.termslash()

    ctx.mkdir(sym, 0o755, err=EEXIST)
    ctx.mkdir(sym, 0o755, err=EEXIST)
