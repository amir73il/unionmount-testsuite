from errno import *
from tool_box import *

###############################################################################
#
# Creation of a not-yet existent file with O_CREAT|O_EXCL and O_TRUNC
#
###############################################################################

# Open read-only
def subtest_1(ctx):
    ctx.begin_test(1, "Create O_CREAT|O_EXCL|O_TRUNC|O_RDONLY")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, ro=1, crt=1, ex=1, tr=1, read="")
    ctx.open_file(f, ro=1, crt=1, ex=1, tr=1, err=EEXIST)
    ctx.open_file(f, ro=1, read="")

# Open write-only and overwrite
def subtest_2(ctx):
    ctx.begin_test(2, "Create O_CREAT|O_EXCL|O_TRUNC|O_WRONLY")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, wo=1, crt=1, ex=1, tr=1, write="q")
    ctx.open_file(f, ro=1, read="q")
    ctx.open_file(f, wo=1, crt=1, ex=1, tr=1, err=EEXIST)
    ctx.open_file(f, ro=1, read="q")

# Open write-only and append
def subtest_3(ctx):
    ctx.begin_test(3, "Create O_CREAT|O_EXCL|O_TRUNC|O_APPEND|O_WRONLY")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, app=1, crt=1, ex=1, tr=1, write="q")
    ctx.open_file(f, ro=1, read="q")
    ctx.open_file(f, app=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(f, ro=1, read="q")

# Open read/write and overwrite
def subtest_4(ctx):
    ctx.begin_test(4, "Create O_CREAT|O_EXCL|O_TRUNC|O_RDWR")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, rw=1, crt=1, ex=1, tr=1, write="q")
    ctx.open_file(f, ro=1, read="q")
    ctx.open_file(f, rw=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(f, ro=1, read="q")

# Open read/write and append
def subtest_5(ctx):
    ctx.begin_test(5, "Create O_CREAT|O_EXCL|O_TRUNC|O_APPEND|O_RDWR")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, ro=1, app=1, crt=1, ex=1, tr=1, write="q")
    ctx.open_file(f, ro=1, read="q")
    ctx.open_file(f, ro=1, app=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(f, ro=1, read="q")

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
]
