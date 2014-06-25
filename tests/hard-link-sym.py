from errno import *

###############################################################################
#
# Try to hardlink symlinks
#
###############################################################################

# Hard link a symlink
def subtest_1(ctx):
    """Hard link symlink"""
    f = ctx.direct_sym() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()

    ctx.link(f, f2)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f2, ro=1, read=":xxx:yyy:zzz")

# Hard link a dangling symlink
def subtest_2(ctx):
    """Hard link dangling symlink"""
    f = ctx.pointless() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()

    ctx.link(f, f2)
    ctx.open_file(f, ro=1, err=ELOOP)
    ctx.open_file(f2, ro=1, err=ELOOP)

# Hard link a non-existent file over a symlink
def subtest_3(ctx):
    """Hard link non-existent file over a symlink"""
    f = ctx.no_file() + ctx.termslash()
    f2 = ctx.direct_sym() + ctx.termslash()

    ctx.link(f, f2, err=ENOENT)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.open_file(f2, ro=1, read=":xxx:yyy:zzz")

# Hard link a symlink over a file
def subtest_4(ctx):
    """Hard link symlink over file"""
    f = ctx.direct_sym() + ctx.termslash()
    f2 = ctx.non_empty_dir() + "/a" + ctx.termslash()

    ctx.link(f, f2, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f2, ro=1, read="")

# Hard link a symlink over a new file
def subtest_5(ctx):
    """Hard link symlink over new file"""
    f = ctx.direct_sym() + ctx.termslash()
    f2 = ctx.reg_file() + "-new" + ctx.termslash()

    ctx.open_file(f2, wo=1, crt=1, write="aaaa")
    ctx.link(f, f2, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f2, ro=1, read="aaaa")

# Hard link a new file over a symlink
def subtest_6(ctx):
    """Hard link new file over symlink"""
    f = ctx.reg_file() + "-new" + ctx.termslash()
    f2 = ctx.direct_sym() + ctx.termslash()

    ctx.open_file(f, wo=1, crt=1, write="aaaa")
    ctx.link(f, f2, err=EEXIST)
    ctx.open_file(f, ro=1, read="aaaa")
    ctx.open_file(f2, ro=1, read=":xxx:yyy:zzz")

# Hard link a symlink over itself
def subtest_7(ctx):
    """Hard link symlink over itself"""
    f = ctx.direct_sym() + ctx.termslash()

    ctx.link(f, f, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Hard link a symlink over another symlink
def subtest_8(ctx):
    """Hard link symlink over another symlink"""
    f = ctx.direct_sym() + ctx.termslash()
    f2 = ctx.pointless() + ctx.termslash()

    ctx.link(f, f2, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f2, ro=1, err=ENOENT)

# Hard link an unlinked symlink
def subtest_9(ctx):
    """Hard link unlinked symlink"""
    f = ctx.direct_sym() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()

    ctx.unlink(f)
    ctx.link(f, f2, err=ENOENT)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.open_file(f2, ro=1, err=ENOENT)

# Hard link a renamed symlink
def subtest_10(ctx):
    """Hard link renamed symlink"""
    f = ctx.direct_sym() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()
    f3 = ctx.no_file() + "-a" + ctx.termslash()

    ctx.rename(f, f2)
    ctx.link(f, f3, err=ENOENT)
    ctx.link(f2, f)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f2, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f3, ro=1, err=ENOENT)
