from errno import *
from tool_box import *

###############################################################################
#
# Unlink tests
#
###############################################################################

def subtest_1(ctx):
    ctx.begin_test(1, "Unlink file")
    f = ctx.reg_file() + ctx.termslash()

    ctx.unlink(f)
    ctx.open_file(f, ro=1, err=ENOENT)

    ctx.unlink(f, err=ENOENT)
    ctx.open_file(f, ro=1, err=ENOENT)

def subtest_2(ctx):
    ctx.begin_test(2, "Unlink direct symlink to file")
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(symlink, ro=1, read=b":xxx:yyy:zzz")
    ctx.unlink(symlink)
    ctx.open_file(symlink, ro=1, err=ENOENT)
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")

    ctx.unlink(symlink, err=ENOENT)
    ctx.open_file(symlink, ro=1, err=ENOENT)
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")

def subtest_3(ctx):
    ctx.begin_test(3, "Unlink indirect symlink to file")
    indirect = ctx.indirect_sym() + ctx.termslash()
    symlink = ctx.direct_sym() + ctx.termslash()
    f = ctx.reg_file() + ctx.termslash()

    ctx.open_file(indirect, ro=1, read=b":xxx:yyy:zzz")
    ctx.unlink(indirect)
    ctx.open_file(indirect, ro=1, err=ENOENT)
    ctx.open_file(symlink, ro=1, read=b":xxx:yyy:zzz")
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")

    ctx.unlink(indirect, err=ENOENT)
    ctx.open_file(indirect, ro=1, err=ENOENT)
    ctx.open_file(symlink, ro=1, read=b":xxx:yyy:zzz")

#
#
#
def subtest_4(ctx):
    ctx.begin_test(4, "Unlink dir")
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.unlink(f, err=EISDIR)
    ctx.open_dir(f, ro=1)

    ctx.unlink(f, err=EISDIR)
    ctx.open_dir(f, ro=1)

def subtest_5(ctx):
    ctx.begin_test(5, "Unlink direct symlink to dir")
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(symlink, ro=1)
    ctx.unlink(symlink)
    if not ctx.termslash():
        ctx.open_dir(symlink, ro=1, err=ENOENT)
    else:
        ctx.open_dir(symlink, ro=1)
    ctx.open_dir(f, ro=1)

    ctx.unlink(symlink, err=ENOENT)
    if not ctx.termslash():
        ctx.open_dir(symlink, ro=1, err=ENOENT)
    else:
        ctx.open_dir(symlink, ro=1)
    ctx.open_dir(f, ro=1)

def subtest_6(ctx):
    ctx.begin_test(6, "Unlink indirect symlink to dir")
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(indirect, ro=1)
    ctx.unlink(indirect)
    if not ctx.termslash():
        ctx.open_dir(indirect, ro=1, err=ENOENT)
    else:
        ctx.open_dir(indirect, ro=1)
    ctx.open_dir(symlink, ro=1)
    ctx.open_dir(f, ro=1)

    ctx.unlink(indirect, err=ENOENT)
    if not ctx.termslash():
        ctx.open_dir(indirect, ro=1, err=ENOENT)
    else:
        ctx.open_dir(indirect, ro=1)
    ctx.open_dir(symlink, ro=1)

#
#
#
def subtest_7(ctx):
    ctx.begin_test(7, "Unlink absent file")
    f = ctx.no_file() + ctx.termslash()

    ctx.unlink(f, err=ENOENT)
    ctx.unlink(f, err=ENOENT)

def subtest_8(ctx):
    ctx.begin_test(8, "Unlink broken symlink to absent file")
    f = ctx.pointless() + ctx.termslash()

    ctx.unlink(f)
    ctx.unlink(f, err=ENOENT)

def subtest_9(ctx):
    ctx.begin_test(9, "Unlink broken symlink")
    f = ctx.pointless() + ctx.termslash()

    ctx.unlink(f)
    ctx.unlink(f, err=ENOENT)

def subtest_10(ctx):
    ctx.begin_test(10, "Unlink absent file pointed to by broken symlink")
    f = ctx.no_file() + ctx.termslash()

    ctx.unlink(f, err=ENOENT)
    ctx.unlink(f, err=ENOENT)

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
