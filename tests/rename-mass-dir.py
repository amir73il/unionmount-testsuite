from errno import *

###############################################################################
#
# Mass rename of directories
#
###############################################################################

ring_size = 7
iter_count = int(ring_size * 4.5)

# Mass create a bunch of sequentially-named directories, and then rename
# through a circular set of names, leaving a gap to move into.  The dirs are
# named 0...ring_size-2 and the gap starts at ring_size-1 and moves backwards.
#
def subtest_1(ctx):
    """Mass rename new sequential dirs circularly"""
    base = ctx.no_dir()[:-3]

    for i in range(0, ring_size - 1):
        path = base + "{:d}".format(100 + i)
        ctx.mkdir(path, 0o755)

    gap = ring_size - 1
    for i in range(0, iter_count):
        next_gap = (gap - 1) % ring_size
        path = base + "{:d}".format(100 + next_gap)
        path2 = base + "{:d}".format(100 + gap)
        ctx.rename(path, path2)
        gap = next_gap

# Delete the previously mass renamed directories
def subtest_2(ctx):
    """Unlink mass renamed dirs"""
    base = ctx.no_dir()[:-3]

    gap = -(iter_count + 1) % ring_size
    for i in range(0, ring_size):
        path = base + "{:d}".format(100 + i)
        if i == gap:
            ctx.rmdir(path, err=ENOENT)
        else:
            ctx.rmdir(path)

# As before, but with populated directories
def subtest_3(ctx):
    """Mass rename new populated sequential dirs circularly"""
    base = ctx.no_dir()[:-3]

    for i in range(0, ring_size - 1):
        path = base + "{:d}".format(100 + i)
        ctx.mkdir(path, 0o755)
        ctx.open_file(path + "/a", wo=1, crt=1, write="abcd{:d}".format(i))

    gap = ring_size - 1
    for i in range(0, iter_count):
        next_gap = (gap - 1) % ring_size
        path = base + "{:d}".format(100 + next_gap)
        path2 = base + "{:d}".format(100 + gap)
        ctx.rename(path, path2)
        gap = next_gap

# Read the files in the previously mass-renamed directories
def subtest_4(ctx):
    """Check files in renamed dirs"""
    base = ctx.no_dir()[:-3]

    # The cycle repeats itself after R * (R-1) iterations
    n = iter_count % (ring_size * (ring_size - 1))

    # The gap is back at the end every R iterations
    cycle = int(n / ring_size)

    # Thus the first number in the sequence in this cycle is...
    n = (ring_size - 1) - cycle

    gap = -(iter_count + 1) % ring_size
    for i in range(0, ring_size):
        if i == gap:
            pass
        else:
            path = base + "{:d}".format(100 + i)
            ctx.open_file(path + "/a", ro=1, read="abcd{:d}".format(n))
            n = (n + 1) % (ring_size - 1)

# Delete the previously mass-renamed directories
def subtest_5(ctx):
    """Unlink mass renamed dirs"""
    base = ctx.no_dir()[:-3]

    gap = -(iter_count + 1) % ring_size
    for i in range(0, ring_size):
        path = base + "{:d}".format(100 + i)
        if i == gap:
            ctx.rmdir(path, err=ENOENT)
        else:
            ctx.unlink(path + "/a")
            ctx.rmdir(path)
