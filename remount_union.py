from tool_box import *

def remount_union(ctx):
    cfg = ctx.config()
    union_mntroot = cfg.union_mntroot()

    if cfg.testing_overlayfs():
        system("umount " + cfg.union_mntroot())
        check_not_tainted()

        lowerlayers = ctx.upper_layer() + ":" + ctx.lower_layers()
        upper_mntroot = cfg.upper_mntroot()
        upperdir = upper_mntroot + "/" + ctx.next_layer()
        os.mkdir(upperdir)
        workdir = upper_mntroot + "/work"
        system("mount -t overlay overlay " + union_mntroot +
               " -onoatime,lowerdir=" + lowerlayers + ",upperdir=" + upperdir + ",workdir=" + workdir)
        ctx.note_lower_layers(lowerlayers)
        ctx.note_upper_layer(upperdir)
