from errno import *
from settings import *
from tool_box import *

###############################################################################
#
# Try to violate permissions
#
###############################################################################

def subtest_1(ctx):
    ctx.begin_test(1, "Impermissible open O_TRUNC|O_WRONLY")
    f = ctx.rootfile() + ctx.termslash()

    ctx.open_file(f, wo=1, tr=1, err=EACCES, as_bin=1)
    ctx.open_file(f, wo=1, err=EACCES, as_bin=1)
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz", as_bin=1)
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")
    ctx.open_file(f, wo=1, write=b"shark")
    ctx.open_file(f, ro=1, read=b"sharkyyy:zzz")
    ctx.open_file(f, ro=1, read=b"sharkyyy:zzz", as_bin=1)

def subtest_2(ctx):
    ctx.begin_test(2, "Impermissible open O_WRONLY")
    f = ctx.rootfile() + ctx.termslash()

    ctx.open_file(f, wo=1, err=EACCES, as_bin=1)
    ctx.open_file(f, wo=1, err=EACCES, as_bin=1)
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz", as_bin=1)
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")
    ctx.open_file(f, wo=1, write=b"shark")
    ctx.open_file(f, ro=1, read=b"sharkyyy:zzz")
    ctx.open_file(f, ro=1, read=b"sharkyyy:zzz", as_bin=1)

def subtest_3(ctx):
    ctx.begin_test(3, "Impermissible open O_APPEND")
    f = ctx.rootfile() + ctx.termslash()

    ctx.open_file(f, app=1, err=EACCES, as_bin=1)
    ctx.open_file(f, app=1, err=EACCES, as_bin=1)
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz", as_bin=1)
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")
    ctx.open_file(f, app=1, write=b"shark")
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzzshark")
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzzshark", as_bin=1)

    #
    #
    #
def subtest_4(ctx):
    ctx.begin_test(4, "Impermissible truncate")
    f = ctx.rootfile() + ctx.termslash()

    if not ctx.termslash():
        size = ctx.get_file_size(f)
        if size != 12:
            raise TestError(f + ": Initial size (" + str(size) + ") is not 12")
    ctx.truncate(f, 4, err=EACCES, as_bin=1)
    ctx.truncate(f, 4, err=EACCES, as_bin=1)
    if not ctx.termslash():
        size = ctx.get_file_size(f)
        if size != 12:
            raise TestError(f + ": Size (" + str(size) + ") is not still 12")
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz", as_bin=1)
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")
    ctx.truncate(f, 4)
    if not ctx.termslash():
        size = ctx.get_file_size(f)
        if size != 4:
            raise TestError(f + ": Size (" + str(size) + ") is not 4")
    ctx.open_file(f, ro=1, read=b":xxx")
    ctx.open_file(f, ro=1, read=b":xxx", as_bin=1)

    #
    #
    #
def subtest_5(ctx):
    ctx.begin_test(5, "Impermissible utimes")
    f = ctx.rootfile() + ctx.termslash()

    if not ctx.termslash():
        atime = ctx.get_file_atime(f)
        mtime = ctx.get_file_mtime(f)
    ctx.utimes(f, err=EACCES, as_bin=1)
    ctx.utimes(f, err=EACCES, as_bin=1)
    if not ctx.termslash():
        if ctx.get_file_atime(file) != atime:
            raise TestError(f + ": Access time unexpectedly changed")
        if ctx.get_file_mtime(file) != mtime:
            raise TestError(f + ": Modification time unexpectedly changed")
    ctx.utimes(f)
    if not ctx.termslash():
        if ctx.get_file_atime(file) == atime:
            raise TestError(f + ": Access time didn't change")
        if ctx.get_file_mtime(file) == mtime:
            raise TestError(f + ": Modification time didn't change")
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
]
