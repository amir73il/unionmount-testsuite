from errno import *

###############################################################################
#
# Open of existing directory; with O_DIRECTORY and create, exclusive and truncate
#
###############################################################################

# Open read-only and create
def subtest_1(ctx):
    """Open O_DIRECTORY | O_RDONLY | O_CREAT"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, ro=1, crt=1, err=EISDIR)
    ctx.open_dir(f, ro=1)

# Open read-only and create exclusive
def subtest_2(ctx):
    """Open O_DIRECTORY | O_RDONLY | O_CREAT | O_EXCL"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, ro=1, crt=1, ex=1, err=EEXIST)
    ctx.open_dir(f, ro=1)

# Open read-only and truncate
def subtest_3(ctx):
    """Open O_DIRECTORY | O_RDONLY | O_TRUNC"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, ro=1, tr=1, err=EISDIR)
    ctx.open_dir(f, ro=1)

# Open read-only and truncate create
def subtest_4(ctx):
    """Open O_DIRECTORY | O_RDONLY | O_TRUNC | O_CREAT"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, ro=1, tr=1, crt=1, err=EISDIR)
    ctx.open_dir(f, ro=1)

# Open read-only and truncate create exclusive
def subtest_5(ctx):
    """Open O_DIRECTORY | O_RDONLY | O_TRUNC | O_CREAT | O_EXCL"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, ro=1, tr=1, crt=1, ex=1, err=EEXIST)
    ctx.open_dir(f, ro=1)

# Open write-only and create
def subtest_6(ctx):
    """Open O_DIRECTORY | O_RDONLY | O_CREAT"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, wo=1, crt=1, err=EISDIR)
    ctx.open_dir(f, ro=1)

# Open write-only and create exclusive
def subtest_7(ctx):
    """Open O_DIRECTORY | O_RDONLY | O_CREAT | O_EXCL"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, wo=1, crt=1, ex=1, err=EEXIST)
    ctx.open_dir(f, ro=1)

# Open write-only and truncate
def subtest_8(ctx):
    """Open O_DIRECTORY | O_RDONLY | O_TRUNC"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, wo=1, tr=1, err=EISDIR)
    ctx.open_dir(f, ro=1)

# Open write-only and truncate create
def subtest_9(ctx):
    """Open O_DIRECTORY | O_RDONLY | O_TRUNC | O_CREAT"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, wo=1, tr=1, crt=1, err=EISDIR)
    ctx.open_dir(f, ro=1)

# Open write-only and truncate create exclusive
def subtest_10(ctx):
    """Open O_DIRECTORY | O_RDONLY | O_TRUNC | O_CREAT | O_EXCL"""
    f = ctx.non_empty_dir() + ctx.termslash()

    ctx.open_dir(f, wo=1, tr=1, crt=1, ex=1, err=EEXIST)
    ctx.open_dir(f, ro=1)
