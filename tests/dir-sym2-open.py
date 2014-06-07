from errno import *
from tool_box import *

###############################################################################
#
# Open through indirect symlink of existing directory; no special flags
#
###############################################################################

# Open(dir symlink) read-only
def subtest_1(ctx):
    ctx.begin_test(1, "Open(dir symlink) O_RDONLY")
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, ro=1)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) write-only and overwrite
def subtest_2(ctx):
    ctx.begin_test(2, "Open(dir symlink) O_WRONLY")
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, wo=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)
    ctx.open_file(indirect, wo=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) write-only and append
def subtest_3(ctx):
    ctx.begin_test(3, "Open(dir symlink) O_APPEND|O_WRONLY")
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, app=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)
    ctx.open_file(indirect, app=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) read/write and overwrite
def subtest_4(ctx):
    ctx.begin_test(4, "Open(dir symlink) O_RDWR")
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, rw=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)
    ctx.open_file(indirect, rw=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) read/write and append
def subtest_5(ctx):
    ctx.begin_test(5, "Open(dir symlink) O_APPEND|O_RDWR")
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, ro=1, app=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)
    ctx.open_file(indirect, ro=1, app=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
]
