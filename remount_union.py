from tool_box import *

def remount_union(ctx, rotate_upper=False):
    cfg = ctx.config()
    union_mntroot = cfg.union_mntroot()
    lower_mntroot = cfg.lower_mntroot()
    snapshot_mntroot = cfg.snapshot_mntroot()
    testdir = cfg.testdir()
    mntopt = cfg.mntopts()

    mnt = union_mntroot
    if cfg.testing_snapshot():
        system("umount " + snapshot_mntroot)
        check_not_tainted()
        mnt = snapshot_mntroot
        mntopt += ",redirect_dir=origin"

    if cfg.testing_overlayfs() or cfg.testing_snapshot():
        system("umount " + cfg.union_mntroot())
        system("echo 3 > /proc/sys/vm/drop_caches")
        check_not_tainted()

        upper_mntroot = cfg.upper_mntroot()
        if rotate_upper and ctx.have_more_layers():
            lowerlayers = ctx.upper_layer() + ":" + ctx.lower_layers()
            layer_mntroot = upper_mntroot + "/" + ctx.next_layer()
            upperdir = layer_mntroot + "/u"
            workdir = layer_mntroot + "/w"
            os.mkdir(layer_mntroot)
            # Create unique fs for upper/N if N < maxfs
            if ctx.have_more_fs():
                system("mount -t tmpfs " + ctx.curr_layer() + "_layer " + layer_mntroot)
            os.mkdir(upperdir)
            os.mkdir(workdir)
            if not cfg.testing_snapshot():
                # Create pure upper file
                write_file(upperdir + "/f", "pure");
        else:
            lowerlayers = ctx.lower_layers()
            layer_mntroot = upper_mntroot + "/" + ctx.curr_layer()
            upperdir = layer_mntroot + "/u"
            workdir = layer_mntroot + "/w"

        cmd = "mount -t " + cfg.fstype() + " " + cfg.fsname() + " " + mnt + " " + mntopt + " -olowerdir=" + lowerlayers + ",upperdir=" + upperdir + ",workdir=" + workdir
        system(cmd)
        if cfg.is_verbose():
            write_kmsg(cmd);
        if cfg.testing_snapshot():
            system("mount -t snapshot " + lower_mntroot + " " + union_mntroot +
                    " -onoatime,snapshot=" + snapshot_mntroot)
            ctx.note_upper_fs(upper_mntroot, testdir, testdir)
        else:
            # Record st_dev of merge dir and pure upper file
            ctx.note_upper_fs(upper_mntroot, testdir, union_mntroot + "/f")
        ctx.note_lower_layers(lowerlayers)
        ctx.note_upper_layer(upperdir)
