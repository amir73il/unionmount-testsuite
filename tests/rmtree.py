from errno import *

# Recursive remove populated dir with lower files
def subtest_1(ctx):
    """Recursive remove populated lower dir with lower files"""
    d = ctx.non_empty_dir() + ctx.termslash()

    ctx.rmtree(d)


