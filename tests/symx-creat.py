from errno import *

###############################################################################
#
# Open through a broken symlink with O_CREAT
#
###############################################################################

# Open/create through broken link read-only
def subtest_1(ctx):
    """Open(broken) O_CREAT|O_RDONLY"""
    symlink = ctx.pointless() + ctx.termslash()
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, crt=1, read="")
    ctx.open_file(f, ro=1, read="")

# Open/create through broken link write-only and overwrite
def subtest_2(ctx):
    """Open(broken) O_CREAT|O_WRONLY"""
    symlink = ctx.pointless() + ctx.termslash()
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(symlink, wo=1, crt=1, write="q")
    ctx.open_file(f, ro=1, read="q")

# Open/create through broken link write-only and append
def subtest_3(ctx):
    """Open(broken) O_CREAT|O_APPEND|O_WRONLY"""
    symlink = ctx.pointless() + ctx.termslash()
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(symlink, app=1, crt=1, write="q")
    ctx.open_file(f, ro=1, read="q")

# Open/create through broken link read/write and overwrite
def subtest_4(ctx):
    """Open(broken) O_CREAT|O_RDWR"""
    symlink = ctx.pointless() + ctx.termslash()
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(symlink, rw=1, crt=1, write="q")
    ctx.open_file(f, ro=1, read="q")

# Open/create through broken link read/write and append
def subtest_5(ctx):
    """Open(broken) O_CREAT|O_APPEND|O_RDWR"""
    symlink = ctx.pointless() + ctx.termslash()
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, app=1, crt=1, write="q")
    ctx.open_file(f, ro=1, read="q")
