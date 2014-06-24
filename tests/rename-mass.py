from errno import *

###############################################################################
#
# Mass rename of files
#
###############################################################################

file_count = 104
iter_count = 3

# Mass rename a bunch of sequentially-named files, where each file in the
# sequence is moved up one, starting from the highest, such that each file is
# renamed to where its successor just was.
def subtest_1(ctx):
    """Mass rename sequential files into each other's vacated name slots"""
    base = ctx.reg_file()[:-3]
    
    for j in range(0, iter_count):
        for i in range(file_count - 1, 100 - 1, -1):
            path = base + "{:d}".format(i + j)
            path2 = base + "{:d}".format(i + j + 1)
            ctx.rename(path, path2)

# Delete the previously mass renamed files
def subtest_2(ctx):
    """Unlink mass renamed files"""
    base = ctx.reg_file()[:-3]

    for i in range(100, file_count):
        path = base + "{:d}".format(i + iter_count)
        ctx.unlink(path)
