from tool_box import *

def remount_union(ctx, rotate_upper=False):
    cfg = ctx.config()
    union_mntroot = cfg.union_mntroot()
    lower_mntroot = cfg.lower_mntroot()
    snapshot_mntroot = cfg.snapshot_mntroot()

    if cfg.testing_snapshot():
        # Unmount old snapshots
        try:
            system("umount " + cfg.snapshot_mntroot() + "/*/ 2>/dev/null")
        except RuntimeError:
            pass
        check_not_tainted()
        # --sn --samefs means start with nosnapshot setup until first recycle
        # so don't add a new layer on first recycle
        if cfg.is_samefs() and ctx.mid_layers() is None:
            rotate_upper = False

    if cfg.testing_overlayfs() or cfg.testing_snapshot():
        system("umount " + cfg.union_mntroot())
        system("echo 3 > /proc/sys/vm/drop_caches")
        check_not_tainted()

        upper_mntroot = cfg.upper_mntroot()
        mid_layers = ctx.mid_layers() or ""
        if rotate_upper and ctx.have_more_layers():
            # Current upper is added to head of overlay mid layers
            mid_layers = ctx.upper_layer() + ":" + mid_layers
            layer_mntroot = upper_mntroot + "/" + ctx.next_layer()
            upperdir = layer_mntroot + "/u"
            workdir = layer_mntroot + "/w"
            os.mkdir(layer_mntroot)
            # Create unique fs for upper/N if N < maxfs
            if ctx.have_more_fs():
                system("mount -t tmpfs " + ctx.curr_layer() + "_layer " + layer_mntroot)
            os.mkdir(upperdir)
            os.mkdir(workdir)
        else:
            layer_mntroot = upper_mntroot + "/" + ctx.curr_layer()
            upperdir = layer_mntroot + "/u"
            workdir = layer_mntroot + "/w"

        mntopt = " -orw" + cfg.mntopts()
        if cfg.testing_snapshot():
            curr_snapshot = snapshot_mntroot + "/" + ctx.curr_layer()
            try:
                os.mkdir(curr_snapshot)
            except OSError:
                pass

            # This is the latest snapshot of lower_mntroot:
            cmd = ("mount -t overlay overlay " + curr_snapshot + mntopt +
                   ",lowerdir=" + lower_mntroot + ",upperdir=" + upperdir + ",workdir=" + workdir)
            system(cmd)
            if cfg.is_verbose():
                write_kmsg(cmd);
            # This is the snapshot mount where tests are run
            system("mount -t snapshot " + lower_mntroot + " " + union_mntroot +
                    " -onoatime,snapshot=" + curr_snapshot)
            # Remount latest snapshot readonly
            system("mount " + curr_snapshot + " -oremount,ro")
            mid_layers = ""
            # Mount old snapshots
            for i in range(ctx.layers_nr() - 1, -1, -1):
                mid_layers = upper_mntroot + "/" + str(i) + ":" + mid_layers
                cmd = ("mount -t overlay overlay " + snapshot_mntroot + "/" + str(i) + "/" +
                       " -oro,lowerdir=" + mid_layers + curr_snapshot)
                system(cmd)
                if cfg.is_verbose():
                    write_kmsg(cmd);
        else:
            cmd = ("mount -t " + cfg.fstype() + " " + cfg.fsname() + " " + union_mntroot + mntopt +
                   ",lowerdir=" + mid_layers + lower_mntroot + ",upperdir=" + upperdir + ",workdir=" + workdir)
            system(cmd)
            if cfg.is_verbose():
                write_kmsg(cmd);
        ctx.note_upper_fs(upper_mntroot, cfg.testdir())
        ctx.note_mid_layers(mid_layers)
        ctx.note_upper_layer(upperdir)
