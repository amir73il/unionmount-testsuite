from errno import *

###############################################################################
#
# Mass rename of symlinks
#
###############################################################################

ring_size = 7
iter_count = int(ring_size * 4.5)

# Mass rename a bunch of sequentially-named symlinks through a circular set of
# names, leaving a gap to move into.  The symlinks are named 0...ring_size-2
# and the gap starts at ring_size-1 and moves backwards.
#
def subtest_1(ctx):
    """Mass rename sequential symlinks circularly"""
    base = ctx.direct_sym()[:-3]

    gap = ring_size - 1
    for i in range(0, iter_count):
        next_gap = (gap - 1) % ring_size
        path = base + "{:d}".format(100 + next_gap)
        path2 = base + "{:d}".format(100 + gap)
        ctx.rename(path, path2)
        gap = next_gap

# Read the previously mass-renamed symlinks
def subtest_2(ctx):
    """Check renamed symlink contents"""
    base = ctx.direct_sym()[:-3]

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
            ctx.readlink(path, content="../a/foo{:d}".format(100 + n))
            ctx.open_file(path, ro=1, read=":xxx:yyy:zzz")
            n = (n + 1) % (ring_size - 1)

# Delete the previously mass-renamed symlinks
def subtest_3(ctx):
    """Unlink mass renamed symlinks"""
    base = ctx.direct_sym()[:-3]

    gap = -(iter_count + 1) % ring_size
    for i in range(0, ring_size + 1):
        path = base + "{:d}".format(100 + i)
        if i == gap:
            ctx.unlink(path, err=ENOENT)
        else:
            ctx.unlink(path)

# As above, but using symlinks to dirs
def subtest_4(ctx):
    """Mass rename sequential dir symlinks circularly"""
    base = ctx.direct_dir_sym()[:-3]

    gap = ring_size - 1
    for i in range(0, iter_count):
        next_gap = (gap - 1) % ring_size
        path = base + "{:d}".format(100 + next_gap)
        path2 = base + "{:d}".format(100 + gap)
        ctx.rename(path, path2)
        gap = next_gap

# Read the previously mass-renamed symlinks
def subtest_5(ctx):
    """Check renamed symlink contents"""
    base = ctx.direct_dir_sym()[:-3]

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
            ctx.readlink(path, content="../a/dir{:d}".format(100 + n))
            ctx.open_dir(path, ro=1)
            n = (n + 1) % (ring_size - 1)

# Delete the previously mass-renamed symlinks
def subtest_6(ctx):
    """Unlink mass renamed symlinks"""
    base = ctx.direct_dir_sym()[:-3]

    gap = -(iter_count + 1) % ring_size
    for i in range(0, ring_size + 1):
        path = base + "{:d}".format(100 + i)
        if i == gap:
            ctx.unlink(path, err=ENOENT)
        else:
            ctx.rmdir(path, err=ENOTDIR)
            ctx.unlink(path)
