from tool_box import *

def remount_union(ctx, rotate_upper=False):
    cfg = ctx.config()
    union_mntroot = None

    if cfg.testing_overlayfs():
        if rotate_upper and ctx.have_more_layers():
            union_mntroot = cfg.union_mntroot()
            system("umount " + union_mntroot)
        check_not_tainted()
        system("exportfs -vu *:/share")
        system("umount -l /share")
        #system("echo 3 > /proc/sys/vm/drop_caches")
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

        cmd = "mount -t overlay overlay /share -onoatime,lowerdir=" + lowerlayers + ",upperdir=" + upperdir + ",workdir=" + workdir
        system(cmd)
        system("exportfs -va")
        if union_mntroot:
            system("mount -t nfs localhost:/share " + union_mntroot)
        if cfg.is_verbose():
            write_kmsg(cmd);
        ctx.note_lower_layers(lowerlayers)
        ctx.note_upper_layer(upperdir)
