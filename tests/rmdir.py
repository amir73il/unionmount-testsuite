from errno import *
from tool_box import *

###############################################################################
#
# Try to remove directories
#
###############################################################################

# Remove a directory that does not exist in the lower layer
def subtest_1(ctx):
    ctx.begin_test(1, "Remove nonexistent directory")
    d = ctx.no_dir() + ctx.termslash()

    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(d, err=ENOENT)

# Remove a subdirectory from a dir that does not exist
def subtest_2(ctx):
    ctx.begin_test(2, "Remove subdir from nonexistent directory")
    d = ctx.no_dir() + "/sub" + ctx.termslash()

    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(d, err=ENOENT)

# Rmdir a file
def subtest_3(ctx):
    ctx.begin_test(3, "Remove-dir a file")
    f = ctx.reg_file()
    d = ctx.reg_file() + ctx.termslash()

    ctx.rmdir(d, err=ENOTDIR)
    ctx.rmdir(d, err=ENOTDIR)
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")

# Remove a subdir from a file
def subtest_4(ctx):
    ctx.begin_test(4, "Remove subdir from file")
    f = ctx.reg_file()
    d = ctx.reg_file() + "/sub" + ctx.termslash()

    ctx.rmdir(d, err=ENOTDIR)
    ctx.rmdir(d, err=ENOTDIR)
    ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")

# Remove an empty lower directory
def subtest_5(ctx):
    ctx.begin_test(5, "Remove empty dir")
    d = ctx.empty_dir() + ctx.termslash()
    subdir = d + "/sub" + ctx.termslash()

    ctx.rmdir(d)
    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(subdir, err=ENOENT)

# Remove a non-existent directory from an empty lower directory
def subtest_6(ctx):
    ctx.begin_test(6, "Remove directory from empty dir")
    d = ctx.empty_dir() + "/sub" + ctx.termslash()

    ctx.rmdir(d, err=ENOENT)
    ctx.rmdir(d, err=ENOENT)

# Remove a populated lower directory
def subtest_7(ctx):
    ctx.begin_test(7, "Remove populated directory")
    d = ctx.non_empty_dir() + ctx.termslash()
    f = d + "/a"

    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.open_file(f, ro=1, read=b"")
    ctx.unlink(f)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.unlink(f, err=ENOENT)
    ctx.rmtree(d)
    ctx.open_file(f, ro=1, read=b"", err=ENOENT)

# Remove a populated lower directory after creating a file in it
def subtest_8(ctx):
    ctx.begin_test(8, "Remove populated directory with created file")
    d = ctx.empty_dir() + ctx.termslash()
    f = d + "/b"

    ctx.open_file(f, wo=1, crt=1, ex=1, write=b"abcq")
    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.unlink(f)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.unlink(f, err=ENOENT)
    ctx.rmtree(d)
    ctx.open_file(f, ro=1, read=b"", err=ENOENT)

# Remove a populated lower directory with copied-up file
def subtest_9(ctx):
    ctx.begin_test(9, "Remove populated directory with copied up file")
    d = ctx.non_empty_dir() + ctx.termslash()
    f = d + "/a"

    ctx.rmdir(d, err=ENOTEMPTY)
    ctx.open_file(f, ro=1, read=b"")
    ctx.open_file(f, wo=1, write=b"abcd")
    ctx.open_file(f, ro=1, read=b"abcd")
    ctx.unlink(f)
    ctx.open_file(f, ro=1, err=ENOENT)
    ctx.unlink(f, err=ENOENT)
    ctx.rmtree(d)
    ctx.open_file(f, ro=1, read=b"", err=ENOENT)

# Remove a populated lower directory after unlinking a file and creating a dir over it
def subtest_10(ctx):
    ctx.begin_test(10, "Remove populated directory with mkdir after unlink")
    d = ctx.non_empty_dir() + ctx.termslash()
    f = d + "/a"

    ctx.rmdir(d, err=ENOTEMPTY)

    ctx.open_file(f, ro=1, read=b"")
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
    ctx.open_file(f, ro=1, read=b"", err=ENOENT)

# Remove a directory from a populated lower directory and recreate it
def subtest_11(ctx):
    ctx.begin_test(11, "Remove directory from dir")
    d = ctx.non_empty_dir() + ctx.termslash()
    pop = d + "/pop"
    subdir = pop + "/c" + ctx.termslash()
    f = pop + "/b"

    ctx.rmdir(subdir)
    ctx.rmdir(subdir, err=ENOENT)
    ctx.mkdir(subdir, 0o755)
    ctx.mkdir(subdir, 0o755, err=EEXIST)
    ctx.open_file(f, ro=1, read=b":aaa:bbb:ccc")

    ctx.rmtree(d)
    ctx.open_file(f, ro=1, err=ENOENT)

# # Remove a directory over a symlink to a file
# def subtest_12(ctx):
#     ctx.begin_test(12, "Remove directory over sym to file")
#     f = ctx.reg_file()
#     d = ctx.reg_file() + ctx.termslash()
#     sym = ctx.direct_sym() + ctx.termslash()

#     ctx.rmdir(sym, err=EEXIST)
#     ctx.rmdir(sym, err=EEXIST)
#     ctx.rmdir(d, err=EEXIST)
#     ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")

# # Remove a directory over a symlink to a symlink to a file
# def subtest_13(ctx):
#     ctx.begin_test(13, "Remove directory over sym to sym to file")
#     f = ctx.reg_file()
#     d = ctx.reg_file() + ctx.termslash()
#     sym = ctx.direct_sym() + ctx.termslash()
#     isym = ctx.indirect_sym() + ctx.termslash()

#     ctx.rmdir(isym, err=EEXIST)
#     ctx.rmdir(isym, err=EEXIST)
#     ctx.rmdir(sym, err=EEXIST)
#     ctx.rmdir(d, err=EEXIST)
#     ctx.open_file(f, ro=1, read=b":xxx:yyy:zzz")

# # Remove a directory over a symlink to a dir
# def subtest_14(ctx):
#     ctx.begin_test(14, "Remove directory over sym to dir")
#     d = ctx.non_empty_dir() + ctx.termslash()
#     sym = ctx.direct_dir_sym() + ctx.termslash()

#     ctx.rmdir(sym, err=EEXIST)
#     ctx.rmdir(sym, err=EEXIST)
#     ctx.rmdir(d, err=EEXIST)
#     ctx.open_file(sym + "/a", ro=1, read=b"")
#     ctx.open_file(d + "/a", ro=1, read=b"")

# # Remove a directory over a symlink to a symlink to a dir
# def subtest_15(ctx):
#     ctx.begin_test(15, "Remove directory over sym to sym to dir")
#     d = ctx.non_empty_dir() + ctx.termslash()
#     sym = ctx.direct_dir_sym() + ctx.termslash()
#     isym = ctx.indirect_dir_sym() + ctx.termslash()

#     ctx.rmdir(isym, err=EEXIST)
#     ctx.rmdir(isym, err=EEXIST)
#     ctx.rmdir(sym, err=EEXIST)
#     ctx.rmdir(d, err=EEXIST)
#     ctx.open_file(isym + "/a", ro=1, read=b"")
#     ctx.open_file(sym + "/a", ro=1, read=b"")
#     ctx.open_file(d + "/a", ro=1, read=b"")

# # Remove a directory over a dangling symlink
# def subtest_16(ctx):
#     ctx.begin_test(16, "Remove directory over dangling sym")
#     d = ctx.no_file() + ctx.termslash()
#     sym = ctx.pointless() + ctx.termslash()

#     ctx.rmdir(sym, err=EEXIST)
#     ctx.rmdir(sym, err=EEXIST)

subtests = [
    subtest_1,
    subtest_2,
    subtest_3,
    subtest_4,
    subtest_5,
    subtest_6,
    subtest_7,
    subtest_8,
    subtest_9,
    subtest_10,
    subtest_11,
    # subtest_12,
    # subtest_13,
    # subtest_14,
    # subtest_15,
    # subtest_16,
]
