from errno import *

###############################################################################
#
# Truncate files
#
###############################################################################

def subtest_1(ctx):
    # Truncate extant file
    """Truncate file"""
    
    key = ":xxx:yyy:zzz"
    while len(key) != 29:
        key += "\0"
    
    for loop in range(0, 29):
        f = ctx.reg_file() + ctx.termslash()

        if not ctx.termslash():
            pre = ctx.get_file_size(f)
            if pre != 12:
                raise TestError(f + ": Initial size (" + str(pre) + ") is not 12")

            ctx.truncate(f, loop)

            post = ctx.get_file_size(f)
            if post != loop:
                raise TestError(f + ": Truncated size (" + str(pre) + ") is not " + str(loop))

            if post != 0:
                ctx.open_file(f, ro=1, read=key[0:loop])
        else:
            ctx.truncate(f, loop, err=ENOTDIR)
        ctx.incr_filenr()
