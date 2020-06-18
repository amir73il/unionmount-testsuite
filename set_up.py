#
# Create and set up a lower layer for the test scripts to use
#
from tool_box import *
import os, shutil

def create_file(name, content):
    fd = open(name, "w")
    fd.write(content)
    fd.close()

# Cleanup old test mounts regardless of the current test setup, because old
# test may have used a different setup (e.g. samefs vs. non-samefs).
def clean_up(cfg):
    base_mntroot = cfg.base_mntroot()
    lower_mntroot = cfg.old_lower_mntroot()
    upper_mntroot = cfg.old_upper_mntroot()
    union_mntroot = cfg.old_union_mntroot()
    snapshot_mntroot = cfg.snapshot_mntroot()

    os.sync()

    try:
        while system("grep -q ' " + union_mntroot + " ' /proc/mounts" +
                     " && umount " + union_mntroot):
            pass
    except RuntimeError:
        pass

    try:
        # Cleanup old overlay snapshot mounts
        while system("grep -q 'overlay " + snapshot_mntroot + "/[0-9]* ' /proc/mounts" +
                     " && umount " + snapshot_mntroot + "/*/ 2>/dev/null"):
            pass
    except RuntimeError:
        pass

    try:
        while system("grep -q 'lower_layer " + lower_mntroot + " ' /proc/mounts" +
                     " && umount " + lower_mntroot):
            pass
    except RuntimeError:
        pass

    try:
        # Cleanup middle/upper/nested layers from [--ov|--ovov] --maxfs=M setup
        while system("grep -q '_layer " + upper_mntroot + "/.[0-9]* ' /proc/mounts" +
                     " && umount " + upper_mntroot + "/* 2>/dev/null"):
            pass
    except RuntimeError:
        pass

    try:
        while system("grep -q '_layer " + upper_mntroot + " ' /proc/mounts" +
                     " && umount " + upper_mntroot):
            pass
    except RuntimeError:
        pass

    try:
        # Cleanup middle/upper/nested layers and overlay mount from setup with basedir
        while system("grep -q ' " + base_mntroot + "/.[0-9]* ' /proc/mounts" +
                     " && umount " + base_mntroot + "/* 2>/dev/null"):
            pass
    except RuntimeError:
        pass

    try:
        # Cleanup basefs mount from --ov --samefs setup
        while system("grep -q 'lower_layer " + base_mntroot + " ' /proc/mounts" +
                     " && umount " + base_mntroot):
            pass
    except RuntimeError:
        pass

def set_up(ctx):
    cfg = ctx.config()
    base_mntroot = cfg.base_mntroot()
    lower_mntroot = cfg.lower_mntroot()
    union_mntroot = cfg.union_mntroot()
    backup_mntroot = cfg.backup_mntroot()
    snapshot_mntroot = cfg.snapshot_mntroot()
    lowerdir = cfg.lowerdir()
    lowerimg = cfg.lowerimg()
    testdir = cfg.testdir()

    if cfg.should_mount_base():
        # Create base fs for all layers and union mount point
        system("mount " + base_mntroot + " 2>/dev/null"
                " || mount -t tmpfs lower_layer " + base_mntroot)
        system("mount --make-private " + base_mntroot)

    if cfg.should_use_base():
        try:
            if lower_mntroot.startswith(base_mntroot):
                os.mkdir(lower_mntroot)
            if union_mntroot.startswith(base_mntroot):
                os.mkdir(union_mntroot)
            if cfg.testing_snapshot():
                os.mkdir(snapshot_mntroot)
                os.mkdir(backup_mntroot)
        except OSError:
            # Cleanup leftover layers from previous run in case base fs is not tmpfs
            if base_mntroot:
                system("rm -rf " + base_mntroot + "/*")
            if lower_mntroot.startswith(base_mntroot):
                os.mkdir(lower_mntroot)
            if union_mntroot.startswith(base_mntroot):
                os.mkdir(union_mntroot)
            if cfg.testing_snapshot():
                os.mkdir(snapshot_mntroot)
                os.mkdir(backup_mntroot)

    if cfg.should_mount_lower():
        # Create a lower layer to union over
        system("mount " + lower_mntroot + " 2>/dev/null"
                " || mount -t tmpfs lower_layer " + lower_mntroot)
        system("mount --make-private " + lower_mntroot)

    #
    # Create a few test files we can use in the lower layer
    #
    try:
        os.mkdir(lowerdir)
    except OSError:
        system("rm -rf " + lowerdir)
        os.mkdir(lowerdir)

    pieces = testdir.split("/")
    del pieces[0]
    path = ""
    for i in pieces:
        path += "/" + i
        ctx.record_file(path, "d")
    ctx.set_cwd(testdir)

    for i in range(100, 130):
        si = str(i)

        # Under the test directory, we create a bunch of regular files
        # containing data called foo100 to foo129:
        create_file(lowerdir + "/foo" + si, ":xxx:yyy:zzz")
        rec = ctx.record_file("foo" + si, "r")

        # Then we create a bunch of direct symlinks to those files
        to = "../a/foo" + si
        os.symlink(to, lowerdir + "/direct_sym" + si)
        rec = ctx.record_file("direct_sym" + si, "s", to, rec)

        # Then we create a bunch of indirect symlinks to those files
        to = "direct_sym" + si
        os.symlink(to, lowerdir + "/indirect_sym" + si)
        ctx.record_file("indirect_sym" + si, "s", to, rec)

        # Then we create a bunch symlinks that don't point to extant files
        to = "no_foo" + si
        os.symlink(to, lowerdir + "/pointless" + si)
        rec = ctx.record_file("no_foo" + si, None)
        ctx.record_file("pointless" + si, "s", to, rec)

        # We create a bunch of directories, each with an empty file
        # and a populated subdir
        os.mkdir(lowerdir + "/dir" + si)
        rec = ctx.record_file("dir" + si, "d")
        create_file(lowerdir + "/dir" + si + "/a", "")
        ctx.record_file("dir" + si + "/a", "f")

        os.mkdir(lowerdir + "/dir" + si + "/pop")
        ctx.record_file("dir" + si + "/pop", "d")
        create_file(lowerdir + "/dir" + si + "/pop/b", ":aaa:bbb:ccc")
        ctx.record_file("dir" + si + "/pop/b", "f")
        os.mkdir(lowerdir + "/dir" + si + "/pop/c")
        ctx.record_file("dir" + si + "/pop/c", "d")

        # And add direct and indirect symlinks to those
        to = "../a/dir" + si
        os.symlink(to, lowerdir + "/direct_dir_sym" + si)
        rec = ctx.record_file("direct_dir_sym" + si, "s", to, rec)
        #ctx.record_file("direct_dir_sym" + si + "/a", "f")

        to = "direct_dir_sym" + si
        os.symlink(to, lowerdir + "/indirect_dir_sym" + si)
        ctx.record_file("indirect_dir_sym" + si, "s", to, rec)
        #ctx.record_file("indirect_dir_sym" + si + "/a", "f")

        # And a bunch of empty directories
        os.mkdir(lowerdir + "/empty" + si)
        ctx.record_file("empty" + si, "d")

        # Everything above is then owned by the bin user
        for f in [ "foo", "direct_sym", "indirect_sym", "pointless" ]:
            os.lchown(lowerdir + "/" + f + si, 1, 1)

        # Create some root-owned regular files also
        create_file(lowerdir + "/rootfile" + si, ":xxx:yyy:zzz")
        ctx.record_file("rootfile" + si, "r")

        # Non-existent dir
        ctx.record_file("no_dir" + si, None)

    if cfg.is_squashfs():
        system("mksquashfs " + lowerdir + " " + lowerimg + " -keep-as-directory > /dev/null");
        system("mount -o loop,ro " + lowerimg + " " + lower_mntroot)
        system("mount --make-private " + lower_mntroot)
    elif cfg.should_mount_lower_ro():
        # Make overlay lower layer read-only
        system("mount -o remount,ro " + lower_mntroot)
    ctx.note_lower_fs(lowerdir)

    if cfg.testing_snapshot():
        # --sn --remount implies start with nosnapshot setup until first recycle
        # so don't make a backup of fs post setup
        if cfg.is_verify():
            if not ctx.remount() or not ctx.recycle():
                ctx.make_backup()
