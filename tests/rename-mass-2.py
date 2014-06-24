from errno import *

###############################################################################
#
# Mass rename of files
#
###############################################################################

file_count = 104
iter_count = 3

# Mass rename a bunch of files, where N is the file number, through
# fooN_0...fooN_M, where M is the number of iterations
def subtest_1(ctx):
    """Mass rename fooN_0->fooN_1->...->fooN_M"""
    base = ctx.reg_file()[:-3]

    for i in range(100, file_count):
        path = base + "{:d}".format(i)
        path2 = path + "_0"
        ctx.rename(path, path2)

    for j in range(0, iter_count):
        for i in range(file_count - 1, 100 - 1, -1):
            path = base + "{:d}_{:d}".format(i, j)
            path2 = base + "{:d}_{:d}".format(i, j + 1)
            ctx.rename(path, path2)

# Delete the previously mass renamed files
def subtest_2(ctx):
    """Unlink mass renamed files"""
    base = ctx.reg_file()[:-3]

    for i in range(100, file_count):
        path = base + "{:d}_{:d}".format(i, iter_count)
        ctx.unlink(path)
