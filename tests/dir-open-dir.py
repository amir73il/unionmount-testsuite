from errno import *

###############################################################################
#
# Open of existing directory; O_DIRECTORY
#
###############################################################################

# Open read-only
def subtest_1(ctx):
    """Open O_DIRECTORY | O_RDONLY"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, ro=1)
    ctx.open_dir(f, ro=1)

# Open write-only and overwrite
def subtest_2(ctx):
    """Open O_DIRECTORY | O_WRONLY"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, wo=1, err=EISDIR)
    ctx.open_dir(f, ro=1)
    ctx.open_dir(f, wo=1, err=EISDIR)
    ctx.open_dir(f, ro=1)

# Open write-only and overwrite twice
def subtest_3(ctx):
    """Open O_DIRECTORY | O_WRONLY * 2"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, wo=1, err=EISDIR)
    ctx.open_dir(f, wo=1, err=EISDIR)
    ctx.open_dir(f, ro=1)

# Open write-only and append
def subtest_4(ctx):
    """Open O_DIRECTORY | O_APPEND|O_WRONLY"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, app=1, err=EISDIR)
    ctx.open_dir(f, ro=1)
    ctx.open_dir(f, app=1, err=EISDIR)
    ctx.open_dir(f, ro=1)

# Open read/write and overwrite
def subtest_5(ctx):
    """Open O_DIRECTORY | O_RDWR"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, rw=1, err=EISDIR)
    ctx.open_dir(f, ro=1)
    ctx.open_dir(f, rw=1, err=EISDIR)
    ctx.open_dir(f, ro=1)

# Open read/write and append
def subtest_6(ctx):
    """Open O_DIRECTORY | O_APPEND|O_RDWR"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, ro=1, app=1, err=EISDIR)
    ctx.open_dir(f, ro=1)
    ctx.open_dir(f, ro=1, app=1, err=EISDIR)
    ctx.open_dir(f, ro=1)
