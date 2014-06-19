from errno import *

###############################################################################
#
# Open through direct symlink of existing directory; no special flags
#
###############################################################################

# Open(dir symlink) read-only
def subtest_1(ctx):
    """Open(dir symlink) O_RDONLY"""
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, ro=1)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) write-only and overwrite
def subtest_2(ctx):
    """Open(dir symlink) O_WRONLY"""
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, wo=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)
    ctx.open_file(symlink, wo=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) write-only and append
def subtest_3(ctx):
    """Open(dir symlink) O_APPEND|O_WRONLY"""
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, app=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)
    ctx.open_file(symlink, app=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) read/write and overwrite
def subtest_4(ctx):
    """Open(dir symlink) O_RDWR"""
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, rw=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)
    ctx.open_file(symlink, rw=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)

# Open(dir symlink) read/write and append
def subtest_5(ctx):
    """Open(dir symlink) O_APPEND|O_RDWR"""
    symlink = ctx.direct_dir_sym() + ctx.termslash()
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(symlink, ro=1, app=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)
    ctx.open_file(symlink, ro=1, app=1, err=EISDIR)
    ctx.open_file(symlink, ro=1)
