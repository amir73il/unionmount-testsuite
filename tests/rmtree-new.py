from errno import *

# Recursive remove populated dir with new subdir
def subtest_1(ctx):
    """Recursive remove populated lower dir with new subdir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    d2 = d + "/b"

    ctx.mkdir(d2, 0o755)
    ctx.rmtree(d)

