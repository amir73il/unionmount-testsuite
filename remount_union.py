from tool_box import *

def remount_union(ctx, rotate_upper=False):
    cfg = ctx.config()
    union_mntroot = cfg.union_mntroot()
    lower_mntroot = cfg.lower_mntroot()
    snapshot_mntroot = cfg.snapshot_mntroot()

    if cfg.testing_snapshot():
        system("umount " + snapshot_mntroot)
        check_not_tainted()
        mnt = snapshot_mntroot
    else:
        mnt = union_mntroot

    if cfg.testing_overlayfs() or cfg.testing_snapshot():
        system("umount " + cfg.union_mntroot())
        system("echo 3 > /proc/sys/vm/drop_caches")
        check_not_tainted()

        upper_mntroot = cfg.upper_mntroot()
        if rotate_upper and ctx.have_more_layers():
            lowerlayers = ctx.upper_layer() + ":" + ctx.lower_layers()
            upperdir = upper_mntroot + "/" + ctx.next_layer()
            workdir = upper_mntroot + "/work" + ctx.curr_layer()
            os.mkdir(upperdir)
            os.mkdir(workdir)
        else:
            lowerlayers = ctx.lower_layers()
            upperdir = ctx.upper_layer()
            workdir = upper_mntroot + "/work" + ctx.curr_layer()

        mntopt = " -orw"
        cmd = "mount -t overlay overlay " + mnt + mntopt + ",lowerdir=" + lowerlayers + ",upperdir=" + upperdir + ",workdir=" + workdir
        system(cmd)
        if cfg.is_verbose():
            write_kmsg(cmd);
        if cfg.testing_snapshot():
            system("mount -t snapshot snapshot " + union_mntroot +
                    " -oupperdir=" + lower_mntroot + ",snapshot=" + snapshot_mntroot)
        ctx.note_lower_layers(lowerlayers)
        ctx.note_upper_layer(upperdir)
