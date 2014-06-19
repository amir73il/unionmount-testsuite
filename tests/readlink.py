from errno import *

###############################################################################
#
# Readlink tests
#
###############################################################################

def subtest_1(ctx):
    """Readlink file"""
    f = ctx.reg_file() + ctx.termslash()

    ctx.readlink(f, err=EINVAL)

def subtest_2(ctx):
    """Readlink direct symlink to file"""
    f = ctx.direct_sym() + ctx.termslash()

    ctx.readlink(f, content=ctx.direct_sym_val())

def subtest_3(ctx):
    """Readlink indirect symlink to file"""
    f = ctx.indirect_sym() + ctx.termslash()

    ctx.readlink(f, content=ctx.indirect_sym_val())

    #
    #
    #
def subtest_4(ctx):
    """Readlink dir"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.readlink(f, err=EINVAL)

def subtest_5(ctx):
    """Readlink direct symlink to dir"""
    f = ctx.direct_dir_sym() + ctx.termslash()

    ctx.readlink(f, content=ctx.direct_dir_sym_val())

def subtest_6(ctx):
    """Readlink indirect symlink to dir"""
    f = ctx.indirect_dir_sym() + ctx.termslash()

    ctx.readlink(f, content=ctx.indirect_dir_sym_val())

    #
    #
    #
def subtest_7(ctx):
    """Readlink absent file"""
    f = ctx.no_file() + ctx.termslash()

    ctx.readlink(f, err=ENOENT)

def subtest_8(ctx):
    """Readlink broken symlink to absent file"""
    f = ctx.pointless() + ctx.termslash()

    ctx.readlink(f, content=ctx.pointless_val())

def subtest_9(ctx):
    """Readlink broken symlink"""
    f = ctx.pointless() + ctx.termslash()

    ctx.readlink(f, content=ctx.pointless_val())

def subtest_10(ctx):
    """Readlink absent file pointed to by broken symlink"""
    f = ctx.no_file() + ctx.termslash()

    ctx.readlink(f, err=ENOENT)
