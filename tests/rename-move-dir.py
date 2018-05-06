from errno import *

###############################################################################
#
# Try to move directories
#
###############################################################################

# Move empty directory into another
def subtest_1(ctx):
    """Move empty dir into another"""
    d = ctx.empty_dir()
    n = d[d.rfind("/"):]
    d = d + ctx.termslash()
    d2 = ctx.non_empty_dir() + ctx.termslash() + n

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_dir(d, ro=1, err=ENOENT)

# Move a populated directory into another
def subtest_2(ctx):
    """Move populated dir into another"""
    d = ctx.non_empty_dir()
    n = d[d.rfind("/"):]
    d = d + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash() + n

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_file(d2 + "/a", ro=1)

# Move a populated directory into another after rename in origin dir
def subtest_3(ctx):
    """Rename populated dir and move into another"""
    d = ctx.non_empty_dir()
    n = d[d.rfind("/"):]
    d2 = d + "x" + ctx.termslash()
    d = d + ctx.termslash()
    d3 = ctx.empty_dir() + ctx.termslash() + n

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2, d3)
    ctx.rename(d2, d3, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d3, ro=1)
    ctx.open_file(d3 + "/a", ro=1)

# Move a populated directory into another and rename in other dir
def subtest_4(ctx):
    """Move populated dir into another and rename"""
    d = ctx.non_empty_dir()
    n = d[d.rfind("/"):]
    d = d + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash() + n
    d3 = ctx.empty_dir() + ctx.termslash() + n + "x"

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2, d3)
    ctx.rename(d2, d3, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d3, ro=1)
    ctx.open_file(d3 + "/a", ro=1)

# Move a populated dir into another and move dir inside it to another
def subtest_5(ctx):
    """Move populated dir into another and move subdir into another"""
    d = ctx.non_empty_dir()
    n = d[d.rfind("/"):]
    d = d + ctx.termslash()
    d2 = ctx.empty_dir() + ctx.termslash() + n
    d2a = d2 + "/pop"
    d3 = ctx.empty_dir() + "/pop"

    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2a, d3)
    ctx.rename(d2a, d3, err=ENOENT)

    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_dir(d2a, ro=1, err=ENOENT)
    ctx.open_dir(d3, ro=1)
    ctx.open_file(d2 + "/a", ro=1)
    ctx.open_file(d3 + "/b", ro=1)

# Move a populated directory into another after rename self and child
def subtest_6(ctx):
    """Rename populated dir and child and move into another"""
    d = ctx.non_empty_dir()
    n = d[d.rfind("/"):]
    d2 = d + "x" + ctx.termslash()
    d2a = d2 + "/pop"
    d = d + ctx.termslash()
    da = d + "/pop"
    db = d + "/popx"
    d3 = ctx.empty_dir() + ctx.termslash() + n
    d3a = d3 + "/pop"
    d3b = d3 + "/popx"

    ctx.rename(da, db, recycle=False)
    ctx.rename(da, db, err=ENOENT)
    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2, d3)
    ctx.rename(d2, d3, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1, err=ENOENT)
    ctx.open_dir(d3, ro=1)
    ctx.open_dir(d3a, ro=1, err=ENOENT)
    ctx.open_dir(d3b, ro=1)
    ctx.open_file(d3 + "/a", ro=1)
    ctx.open_file(d3b + "/b", ro=1)

# Move a populated directory into another after rename self and parent
def subtest_7(ctx):
    """Rename populated dir and parent and move into another"""
    d = ctx.non_empty_dir()
    n = d[d.rfind("/"):]
    d2 = d + "x" + ctx.termslash()
    d2a = d2 + "/pop"
    d2b = d2 + "/popx"
    d = d + ctx.termslash()
    da = d + "/pop"
    db = d + "/popx"
    d3 = ctx.empty_dir() + ctx.termslash()
    d3a = d3 + "/pop"
    d3b = d3 + "/popx"

    ctx.rename(da, db, recycle=False)
    ctx.rename(da, db, err=ENOENT)
    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.rename(d2b, d3b)
    ctx.rename(d2b, d3b, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_dir(d2a, ro=1, err=ENOENT)
    ctx.open_dir(d2b, ro=1, err=ENOENT)
    ctx.open_dir(d3, ro=1)
    ctx.open_dir(d3a, ro=1, err=ENOENT)
    ctx.open_dir(d3b, ro=1)
    ctx.open_file(d2 + "/a", ro=1)
    ctx.open_file(d3b + "/b", ro=1)

# Move a new empty directory into an empty lower dir
def subtest_8(ctx):
    """Move new empty dir into empty lower"""
    d = ctx.empty_dir() + "-new" + ctx.termslash()
    d2 = ctx.empty_dir() + "/new" + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, d2)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)

# Move a new empty directory into lower ancestor
def subtest_9(ctx):
    """Move new empty dir into lower ancestor"""
    d = ctx.empty_dir() + "/new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(d, 0o755)
    ctx.rename(d, d2)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)

# Move a new directory leaf into lower ancestor
def subtest_10(ctx):
    """Move new dir leaf into lower ancestor"""
    p = ctx.empty_dir() + "/newp"
    d = p + "/new" + ctx.termslash()
    d2 = ctx.no_dir() + ctx.termslash()

    ctx.mkdir(p, 0o755)
    ctx.mkdir(d, 0o755)
    ctx.rename(d, d2)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)

# Move a new directory branch into lower ancestor
def subtest_11(ctx):
    """Move new dir branch into lower ancestor"""
    p = ctx.empty_dir() + "/newp"
    d = p + "/new" + ctx.termslash()
    n = ctx.no_dir()
    d2 = n + ctx.termslash()

    ctx.mkdir(p, 0o755)
    ctx.mkdir(d, 0o755)
    ctx.rename(p, d2)
    ctx.open_dir(p, ro=1, err=ENOENT)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_dir(n + "/new", ro=1)

# Move a populated directory into a new dir
def subtest_12(ctx):
    """Move populated dir into a new dir"""
    d = ctx.non_empty_dir()
    n = d[d.rfind("/"):]
    d = d + ctx.termslash()
    p = ctx.empty_dir() + "/new" + ctx.termslash()
    d2 = p + n + ctx.termslash()

    ctx.mkdir(p, 0o755)
    ctx.rename(d, d2)
    ctx.rename(d, d2, err=ENOENT)
    ctx.open_dir(d2, ro=1)
    ctx.open_dir(d, ro=1, err=ENOENT)
    ctx.open_file(d2 + "/a", ro=1)
