from errno import *
from settings import *
from tool_box import *

###############################################################################
#
# Open through direct symlink of existing directory; with create, exclusive and
# truncate
#
###############################################################################

# Open(dir symlink) read-only and create
def subtest_1(ctx):
    ctx.begin_test(1, "Open(dir symlink) O_RDONLY | O_CREAT")
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, ro=1, crt=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) read-only and create exclusive
def subtest_2(ctx):
    ctx.begin_test(2, "Open(dir symlink) O_RDONLY | O_CREAT | O_EXCL")
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, ro=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) read-only and truncate
def subtest_3(ctx):
    ctx.begin_test(3, "Open(dir symlink) O_RDONLY | O_TRUNC")
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, ro=1, tr=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) read-only and truncate create
def subtest_4(ctx):
    ctx.begin_test(4, "Open(dir symlink) O_RDONLY | O_TRUNC | O_CREAT")
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, ro=1, tr=1, crt=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) read-only and truncate create exclusive
def subtest_5(ctx):
    ctx.begin_test(5, "Open(dir symlink) O_RDONLY | O_TRUNC | O_CREAT | O_EXCL")
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, ro=1, tr=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) write-only and create
def subtest_6(ctx):
    ctx.begin_test(6, "Open(dir symlink) O_WRONLY | O_CREAT")
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, wo=1, crt=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) write-only and create exclusive
def subtest_7(ctx):
    ctx.begin_test(7, "Open(dir symlink) O_WRONLY | O_CREAT | O_EXCL")
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, wo=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) write-only and truncate
def subtest_8(ctx):
    ctx.begin_test(8, "Open(dir symlink) O_WRONLY | O_TRUNC")
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, wo=1, tr=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) write-only and truncate create
def subtest_9(ctx):
    ctx.begin_test(9, "Open(dir symlink) O_WRONLY | O_TRUNC | O_CREAT")
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, wo=1, tr=1, crt=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) write-only and truncate create exclusive
def subtest_10(ctx):
    ctx.begin_test(10, "Open(dir symlink) O_WRONLY | O_TRUNC | O_CREAT | O_EXCL")
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, wo=1, tr=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(symlink, ro=1)

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
