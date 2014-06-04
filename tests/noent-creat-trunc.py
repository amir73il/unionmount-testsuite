from errno import *
from settings import *
from tool_box import *

###############################################################################
#
# Creation of a not-yet existent file with O_CREAT and O_TRUNC
#
###############################################################################

# Open read-only
def subtest_1(ctx):
    ctx.begin_test(1, "Create O_CREAT|O_TRUNC|O_RDONLY")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, ro=1, crt=1, tr=1, read=b"")
    ctx.open_file(f, ro=1, crt=1, tr=1, read=b"")

# Open write-only and overwrite
def subtest_2(ctx):
    ctx.begin_test(2, "Create O_CREAT|O_TRUNC|O_WRONLY")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, wo=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")
    ctx.open_file(f, wo=1, crt=1, tr=1, write=b"p")
    ctx.open_file(f, ro=1, read=b"p")

# Open write-only and append
def subtest_3(ctx):
    ctx.begin_test(3, "Create O_CREAT|O_TRUNC|O_APPEND|O_WRONLY")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, app=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")
    ctx.open_file(f, app=1, crt=1, write=b"p")
    ctx.open_file(f, ro=1, read=b"qp")

# Open read/write and overwrite
def subtest_4(ctx):
    ctx.begin_test(4, "Create O_CREAT|O_TRUNC|O_RDWR")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, rw=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")
    ctx.open_file(f, rw=1, crt=1, write=b"p")
    ctx.open_file(f, ro=1, read=b"p")

# Open read/write and append
def subtest_5(ctx):
    ctx.begin_test(5, "Create O_CREAT|O_TRUNC|O_APPEND|O_RDWR")
    f = ctx.no_file() + ctx.termslash()

    ctx.open_file(f, ro=1, app=1, crt=1, tr=1, write=b"q")
    ctx.open_file(f, ro=1, read=b"q")
    ctx.open_file(f, ro=1, app=1, crt=1, write=b"p")
    ctx.open_file(f, ro=1, read=b"qp")

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
]
