from errno import *

###############################################################################
#
# Try to remove directories
#
###############################################################################

# Remove a directory that does not exist in the lower layer
def subtest_1(ctx):
    """Remove nonexistent directory"""
    d = ctx.no_dir() + ctx.termslash()

    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(d, err=ENOENT)

# Remove a subdirectory from a dir that does not exist
def subtest_2(ctx):
    """Remove subdir from nonexistent directory"""
    d = ctx.no_dir() + "/sub" + ctx.termslash()

    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(d, err=ENOENT)

# Rmdir a file
def subtest_3(ctx):
    """Remove-dir a file"""
    f = ctx.reg_file()
    d = ctx.reg_file() + ctx.termslash()

    ctx.rmdir(d, err=ENOTDIR)
    ctx.rmdir(d, err=ENOTDIR)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Remove a subdir from a file
def subtest_4(ctx):
    """Remove subdir from file"""
    f = ctx.reg_file()
    d = ctx.reg_file() + "/sub" + ctx.termslash()

    ctx.rmdir(d, err=ENOTDIR)
    ctx.rmdir(d, err=ENOTDIR)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Remove an empty lower directory
def subtest_5(ctx):
    """Remove empty dir"""
    d = ctx.empty_dir() + ctx.termslash()
    subdir = d + "/sub" + ctx.termslash()

    ctx.rmdir(d)
    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(subdir, err=ENOENT)

# Remove a non-existent directory from an empty lower directory
def subtest_6(ctx):
    """Remove directory from empty dir"""
    d = ctx.empty_dir() + "/sub" + ctx.termslash()

    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(d, err=ENOENT)

# Remove a populated lower directory
def subtest_7(ctx):
    """Remove populated directory"""
    d = ctx.non_empty_dir() + ctx.termslash()
    f = d + "/a"

    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.open_file(f, ro=1, read="")
    ctx.unlink(f)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.unlink(f, err=ENOENT)
    ctx.rmtree(d)
    ctx.open_file(f, ro=1, read="", err=ENOENT)

# Remove a populated lower directory after creating a file in it
def subtest_8(ctx):
    """Remove populated directory with created file"""
    d = ctx.empty_dir() + ctx.termslash()
    f = d + "/b"

    ctx.open_file(f, wo=1, crt=1, ex=1, write="abcq")
    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.unlink(f)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.unlink(f, err=ENOENT)
    ctx.rmtree(d)
    ctx.open_file(f, ro=1, read="", err=ENOENT)

# Remove a populated lower directory with copied-up file
def subtest_9(ctx):
    """Remove populated directory with copied up file"""
    d = ctx.non_empty_dir() + ctx.termslash()
    f = d + "/a"

    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.open_file(f, ro=1, read="")
    ctx.open_file(f, wo=1, write="abcd")
    ctx.open_file(f, ro=1, read="abcd")
    ctx.unlink(f)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.unlink(f, err=ENOENT)
    ctx.rmtree(d)
    ctx.open_file(f, ro=1, read="", err=ENOENT)

# Remove a populated lower directory after unlinking a file and creating a dir over it
def subtest_10(ctx):
    """Remove populated directory with mkdir after unlink"""
    d = ctx.non_empty_dir() + ctx.termslash()
    f = d + "/a"

    ctx.rmdir(d, err=ENOTEMPTY)

    ctx.open_file(f, ro=1, read="")
    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.unlink(f)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.unlink(f, err=ENOENT)

    ctx.mkdir(f, 0o755)
    ctx.mkdir(f, 0o755, err=EEXIST)
    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.rmdir(f)
    ctx.rmdir(f, err=ENOENT)

    ctx.rmtree(d)
    ctx.open_file(f, ro=1, read="", err=ENOENT)

# Remove a directory from a populated lower directory and recreate it
def subtest_11(ctx):
    """Remove directory from dir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    pop = d + "/pop"
    subdir = pop + "/c" + ctx.termslash()
    f = pop + "/b"

    ctx.rmdir(subdir)
    ctx.rmdir(subdir, err=ENOENT)
    ctx.mkdir(subdir, 0o755)
    ctx.mkdir(subdir, 0o755, err=EEXIST)
    ctx.open_file(f, ro=1, read=":aaa:bbb:ccc")

    ctx.rmtree(d)
    ctx.open_file(f, ro=1, err=ENOENT)

# Remove directory symlinks pointing to a file
def subtest_12(ctx):
    """Remove-dir symlinks to file"""
    f = ctx.reg_file()
    d = ctx.reg_file() + ctx.termslash()
    sym = ctx.direct_sym() + ctx.termslash()
    isym = ctx.indirect_sym() + ctx.termslash()

    ctx.rmdir(isym, err=ENOTDIR)
    ctx.rmdir(isym, err=ENOTDIR)
    ctx.rmdir(sym, err=ENOTDIR)
    ctx.rmdir(sym, err=ENOTDIR)
    ctx.rmdir(d, err=ENOTDIR)
    ctx.rmdir(d, err=ENOTDIR)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")

# Remove a directory over a symlink to a dir
def subtest_13(ctx):
    """Remove directory over sym to dir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    sym = ctx.direct_dir_sym() + ctx.termslash()

    ctx.rmdir(sym, err=ENOTDIR)
    ctx.rmdir(sym, err=ENOTDIR)
    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.open_file(sym + "/a", ro=1, read="")
    ctx.open_file(d + "/a", ro=1, read="")
    ctx.rmtree(d)
    ctx.open_file(sym + "/a", ro=1, err=ENOENT)
    ctx.open_file(d + "/a", ro=1, err=ENOENT)

# Remove a directory over a symlink to a symlink to a dir
def subtest_14(ctx):
    """Remove directory over sym to sym to dir"""
    d = ctx.non_empty_dir() + ctx.termslash()
    sym = ctx.direct_dir_sym() + ctx.termslash()
    isym = ctx.indirect_dir_sym() + ctx.termslash()

    ctx.rmdir(isym, err=ENOTDIR)
    ctx.rmdir(isym, err=ENOTDIR)
    ctx.rmdir(sym, err=ENOTDIR)
    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.open_file(isym + "/a", ro=1, read="")
    ctx.open_file(sym + "/a", ro=1, read="")
    ctx.open_file(d + "/a", ro=1, read="")
    ctx.rmtree(d)
    ctx.open_file(isym + "/a", ro=1, err=ENOENT)
    ctx.open_file(sym + "/a", ro=1, err=ENOENT)
    ctx.open_file(d + "/a", ro=1, err=ENOENT)

# Remove a directory over a dangling symlink
def subtest_15(ctx):
    """Remove directory over dangling sym"""
    d = ctx.no_file() + ctx.termslash()
    sym = ctx.pointless() + ctx.termslash()

    ctx.rmdir(sym, err=ENOTDIR)
    ctx.rmdir(sym, err=ENOTDIR)
    ctx.rmdir(d, err=ENOENT)

# Remove an empty lower directory, recreate, populate and try to remove
def subtest_16(ctx):
    """Remove non-empty opaque directory"""
    d = ctx.empty_dir() + ctx.termslash()
    f = d + "/b"

    ctx.rmdir(d)
    ctx.rmdir(d, err=ENOENT)
    ctx.mkdir(d, 0o755)
    ctx.open_file(f, wo=1, crt=1, ex=1, write="abcq")
    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.unlink(f)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.unlink(f, err=ENOENT)
    ctx.rmdir(d)
