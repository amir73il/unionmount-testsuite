from errno import *

###############################################################################
#
# Mass rename of files
#
###############################################################################

ring_size = 7
iter_count = int(ring_size * 4.5)

# Mass hardlink a bunch of sequentially-named files, and then rename through a
# circular set of names, leaving a gap to move into.  The files are named
# 0...ring_size-2 and the gap starts at ring_size-1 and moves backwards.
#
def subtest_1(ctx):
    """Mass rename hardlinked sequential files circularly"""
    src_base = ctx.reg_file()[:-3]
    base = ctx.no_file()[:-3]

    for i in range(0, ring_size + 1):
        src = src_base + "{:d}".format(100 + i)
        path = base + "{:d}".format(100 + i)
        ctx.link(src, path)

    gap = ring_size - 1
    for i in range(0, iter_count):
        next_gap = (gap - 1) % ring_size
        path = base + "{:d}".format(100 + next_gap)
        path2 = base + "{:d}".format(100 + gap)
        ctx.rename(path, path2)
        gap = next_gap

    gap = ring_size - 1
    for i in range(0, iter_count):
        next_gap = (gap + 1) % ring_size
        path = src_base + "{:d}".format(100 + next_gap)
        path2 = src_base + "{:d}".format(100 + gap)
        ctx.rename(path, path2)
        gap = next_gap

# Delete the previously mass renamed files
def subtest_2(ctx):
    """Unlink mass renamed files"""
    src_base = ctx.reg_file()[:-3]
    base = ctx.no_file()[:-3]

    gap = -(iter_count + 1) % ring_size
    for i in range(0, ring_size + 1):
        path = base + "{:d}".format(100 + i)
        if i == gap:
            ctx.unlink(path, err=ENOENT)
        else:
            ctx.unlink(path)

    gap = (iter_count - 1) % ring_size
    for i in range(0, ring_size + 1):
        src = src_base + "{:d}".format(100 + i)
        if i == gap:
            ctx.unlink(src, err=ENOENT)
        else:
            ctx.unlink(src)
