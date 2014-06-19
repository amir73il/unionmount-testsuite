from errno import *

###############################################################################
#
# Open through indirect symlink of existing directory; with create, exclusive
# and truncate
#
###############################################################################

# Open(dir symlink) read-only and create
def subtest_1(ctx):
    """Open(dir symlink) O_RDONLY | O_CREAT"""
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, ro=1, crt=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) read-only and create exclusive
def subtest_2(ctx):
    """Open(dir symlink) O_RDONLY | O_CREAT | O_EXCL"""
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, ro=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) read-only and truncate
def subtest_3(ctx):
    """Open(dir symlink) O_RDONLY | O_TRUNC"""
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, ro=1, tr=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) read-only and truncate create
def subtest_4(ctx):
    """Open(dir symlink) O_RDONLY | O_TRUNC | O_CREAT"""
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, ro=1, tr=1, crt=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) read-only and truncate create exclusive
def subtest_5(ctx):
    """Open(dir symlink) O_RDONLY | O_TRUNC | O_CREAT | O_EXCL"""
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, ro=1, tr=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) write-only and create
def subtest_6(ctx):
    """Open(dir symlink) O_WRONLY | O_CREAT"""
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, wo=1, crt=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) write-only and create exclusive
def subtest_7(ctx):
    """Open(dir symlink) O_WRONLY | O_CREAT | O_EXCL"""
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, wo=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) write-only and truncate
def subtest_8(ctx):
    """Open(dir symlink) O_WRONLY | O_TRUNC"""
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, wo=1, tr=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) write-only and truncate create
def subtest_9(ctx):
    """Open(dir symlink) O_WRONLY | O_TRUNC | O_CREAT"""
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, wo=1, tr=1, crt=1, err=EISDIR)
    ctx.open_file(indirect, ro=1)

# Open(dir symlink) write-only and truncate create exclusive
def subtest_10(ctx):
    """Open(dir symlink) O_WRONLY | O_TRUNC | O_CREAT | O_EXCL"""
    indirect = ctx.indirect_dir_sym() + ctx.termslash()
    direct = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(indirect, wo=1, tr=1, crt=1, ex=1, err=EEXIST)
    ctx.open_file(indirect, ro=1)
