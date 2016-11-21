from tool_box import *

def remount_union(ctx):
    cfg = ctx.config()
    union_mntroot = cfg.union_mntroot()

    if cfg.testing_overlayfs():
        system("umount " + cfg.union_mntroot())
        check_not_tainted()

        if ctx.have_more_layers():
            lowerlayers = ctx.upper_layer() + ":" + ctx.lower_layers()
        else:
            lowerlayers = ctx.lower_layers()
        upper_mntroot = cfg.upper_mntroot()
        if ctx.have_more_layers():
            upperdir = upper_mntroot + "/" + ctx.next_layer()
            os.mkdir(upperdir)
        else:
            upperdir = ctx.upper_layer()
        workdir = upper_mntroot + "/work"
        mnt = union_mntroot
        cmd = "mount -t overlay overlay " + mnt + " -onoatime,lowerdir=" + lowerlayers + ",upperdir=" + upperdir + ",workdir=" + workdir
        system(cmd)
        write_file("/dev/kmsg", cmd);
        ctx.note_lower_layers(lowerlayers)
        ctx.note_upper_layer(upperdir)
