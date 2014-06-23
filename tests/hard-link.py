from errno import *

###############################################################################
#
# Try to hardlink files
#
###############################################################################

# Hard link a file
def subtest_1(ctx):
    """Hard link file"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()

    ctx.link(f, f2)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f2, ro=1, read=":xxx:yyy:zzz")

# Hard link a non-existent file
def subtest_2(ctx):
    """Hard link non-existent file"""
    f = ctx.no_file() + ctx.termslash()
    f2 = ctx.no_file() + "a" + ctx.termslash()

    ctx.link(f, f2, err=ENOENT)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.open_file(f2, ro=1, err=ENOENT)

# Hard link a non-existent file over a real file
def subtest_3(ctx):
    """Hard link non-existent file over a file"""
    f = ctx.no_file() + ctx.termslash()
    f2 = ctx.reg_file() + ctx.termslash()

    ctx.link(f, f2, err=ENOENT)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.open_file(f2, ro=1, read=":xxx:yyy:zzz")

# Hard link a file over another file
def subtest_4(ctx):
    """Hard link file over file"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.non_empty_dir() + "/a" + ctx.termslash()

    ctx.link(f, f2, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f2, ro=1, read="")

# Hard link a file over a new file
def subtest_5(ctx):
    """Hard link file over new file"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.reg_file() + "-new" + ctx.termslash()

    ctx.open_file(f2, wo=1, crt=1, write="aaaa")
    ctx.link(f, f2, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f2, ro=1, read="aaaa")

# Hard link a new file over a lower file
def subtest_6(ctx):
    """Hard link new file over lower file"""
    f = ctx.reg_file() + "-new" + ctx.termslash()
    f2 = ctx.reg_file() + ctx.termslash()

    ctx.open_file(f, wo=1, crt=1, write="aaaa")
    ctx.link(f, f2, err=EEXIST)
    ctx.open_file(f, ro=1, read="aaaa")
    ctx.open_file(f2, ro=1, read=":xxx:yyy:zzz")

# Hard link a file over itself
def subtest_7(ctx):
    """Hard link file over itself"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.link(f, f, err=EEXIST)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Hard link a new file over itself
def subtest_8(ctx):
    """Hard link new file over itself"""
    f = ctx.reg_file() + "-new" + ctx.termslash()

    ctx.open_file(f, wo=1, crt=1, write="aaaa")
    ctx.link(f, f, err=EEXIST)
    ctx.open_file(f, ro=1, read="aaaa")

# Hard link a non-existent file over itself
def subtest_9(ctx):
    """Hard link non-existent file over itself"""
    f = ctx.no_file() + ctx.termslash()

    ctx.link(f, f, err=ENOENT)
    ctx.open_file(f, ro=1, err=ENOENT)

# Hard link an unlinked file
def subtest_10(ctx):
    """Hard link unlinked file"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()

    ctx.unlink(f)
    ctx.link(f, f2, err=ENOENT)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.open_file(f2, ro=1, err=ENOENT)

# Hard link a renamed file
def subtest_11(ctx):
    """Hard link renamed file"""
    f = ctx.reg_file() + ctx.termslash()
    f2 = ctx.no_file() + ctx.termslash()
    f3 = ctx.no_file() + "-a" + ctx.termslash()

    ctx.rename(f, f2)
    ctx.link(f, f3, err=ENOENT)
    ctx.link(f2, f)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f2, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f3, ro=1, err=ENOENT)
