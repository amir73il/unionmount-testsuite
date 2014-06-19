from errno import *

###############################################################################
#
# Open of existing directory; no special flags
#
###############################################################################

# Open read-only
def subtest_1(ctx):
    """Open O_RDONLY"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, ro=1)
    ctx.open_file(f, ro=1)

# Open write-only and overwrite
def subtest_2(ctx):
    """Open O_WRONLY"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, wo=1, err=EISDIR)
    ctx.open_file(f, ro=1)
    ctx.open_file(f, wo=1, err=EISDIR)
    ctx.open_file(f, ro=1)

# Open write-only and overwrite twice
def subtest_3(ctx):
    """Open O_WRONLY * 2"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, wo=1, err=EISDIR)
    ctx.open_file(f, wo=1, err=EISDIR)
    ctx.open_file(f, ro=1)

# Open write-only and append
def subtest_4(ctx):
    """Open O_APPEND|O_WRONLY"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, app=1, err=EISDIR)
    ctx.open_file(f, ro=1)
    ctx.open_file(f, app=1, err=EISDIR)
    ctx.open_file(f, ro=1)

# Open read/write and overwrite
def subtest_5(ctx):
    """Open O_RDWR"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, rw=1, err=EISDIR)
    ctx.open_file(f, ro=1)
    ctx.open_file(f, rw=1, err=EISDIR)
    ctx.open_file(f, ro=1)

# Open read/write and append
def subtest_6(ctx):
    """Open O_APPEND|O_RDWR"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_file(f, ro=1, app=1, err=EISDIR)
    ctx.open_file(f, ro=1)
    ctx.open_file(f, ro=1, app=1, err=EISDIR)
    ctx.open_file(f, ro=1)
