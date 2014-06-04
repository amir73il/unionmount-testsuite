from errno import *
from settings import *
from tool_box import *

###############################################################################
#
# Readlink tests
#
###############################################################################

def subtest_1(ctx):
    ctx.begin_test(1, "Readlink file")
    f = ctx.reg_file() + ctx.termslash()

    ctx.readlink(f, err=EINVAL)

def subtest_2(ctx):
    ctx.begin_test(2, "Readlink direct symlink to file")
    f = ctx.direct_sym() + ctx.termslash()

    ctx.readlink(f, content=ctx.direct_sym_val())

def subtest_3(ctx):
    ctx.begin_test(3, "Readlink indirect symlink to file")
    f = ctx.indirect_sym() + ctx.termslash()

    ctx.readlink(f, content=ctx.indirect_sym_val())

    #
    #
    #
def subtest_4(ctx):
    ctx.begin_test(4, "Readlink dir")
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.readlink(f, err=EINVAL)

def subtest_5(ctx):
    ctx.begin_test(5, "Readlink direct symlink to dir")
    f = ctx.direct_dir_sym() + ctx.termslash()

    ctx.readlink(f, content=ctx.direct_dir_sym_val())

def subtest_6(ctx):
    ctx.begin_test(6, "Readlink indirect symlink to dir")
    f = ctx.indirect_dir_sym() + ctx.termslash()

    ctx.readlink(f, content=ctx.indirect_dir_sym_val())

    #
    #
    #
def subtest_7(ctx):
    ctx.begin_test(7, "Readlink absent file")
    f = ctx.no_file() + ctx.termslash()

    ctx.readlink(f, err=ENOENT)

def subtest_8(ctx):
    ctx.begin_test(8, "Readlink broken symlink to absent file")
    f = ctx.pointless() + ctx.termslash()

    ctx.readlink(f, content=ctx.pointless_val())

def subtest_9(ctx):
    ctx.begin_test(9, "Readlink broken symlink")
    f = ctx.pointless() + ctx.termslash()

    ctx.readlink(f, content=ctx.pointless_val())

def subtest_10(ctx):
    ctx.begin_test(10, "Readlink absent file pointed to by broken symlink")
    f = ctx.no_file() + ctx.termslash()

    ctx.readlink(f, err=ENOENT)

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
    subtest_6,
    subtest_7,
    subtest_8,
    subtest_9,
    subtest_10,
]
