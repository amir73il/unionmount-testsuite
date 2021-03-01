from tool_box import *

def remount_union(ctx, rotate_upper=False):
    cfg = ctx.config()
    union_mntroot = cfg.union_mntroot()
    lower_mntroot = cfg.lower_mntroot()
    snapshot_mntroot = cfg.snapshot_mntroot()
    testdir = cfg.testdir()
    mntopt = cfg.mntopts()

    if cfg.testing_snapshot():
        # Unmount old snapshots
        try:
            system("umount " + snapshot_mntroot + "/*/ 2>/dev/null")
        except RuntimeError:
            pass
        check_not_tainted()

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
            if not cfg.testing_snapshot():
                # Create pure upper file
                write_file(upperdir + "/f", "pure");
        else:
            layer_mntroot = upper_mntroot + "/" + ctx.curr_layer()
            upperdir = layer_mntroot + "/u"
            workdir = layer_mntroot + "/w"

        if cfg.testing_snapshot():
            curr_snapshot = snapshot_mntroot + "/" + ctx.curr_layer()
            try:
                os.mkdir(curr_snapshot)
            except OSError:
                pass

            mntopt += ",redirect_dir=origin"
            # This is the latest snapshot of lower_mntroot:
            cmd = ("mount -t overlay overlay " + curr_snapshot + " " + mntopt +
                   " -olowerdir=" + lower_mntroot + ",upperdir=" + upperdir + ",workdir=" + workdir)
            system(cmd)
            if cfg.is_verbose():
                write_kmsg(cmd);
            # This is the snapshot mount where tests are run
            system("mount -t snapshot " + lower_mntroot + " " + union_mntroot +
                    " -onoatime,snapshot=" + curr_snapshot)
            ctx.note_upper_fs(upper_mntroot, testdir, testdir)

            # Remount latest snapshot readonly
            system("mount " + curr_snapshot + " -oremount,ro")
            mid_layers = ""
            # Mount old snapshots
            for i in range(ctx.layers_nr() - 1, -1, -1):
                mid_layers = upper_mntroot + "/" + str(i) + "/u:" + mid_layers
                cmd = ("mount -t overlay overlay " + snapshot_mntroot + "/" + str(i) + "/" +
                       " -oro,lowerdir=" + mid_layers + curr_snapshot)
                system(cmd)
                if cfg.is_verbose():
                    write_kmsg(cmd);
        else:
            cmd = ("mount -t " + cfg.fstype() + " " + cfg.fsname() + " " + union_mntroot + " " + mntopt +
                   " -olowerdir=" + mid_layers + ctx.lower_layer() + ",upperdir=" + upperdir + ",workdir=" + workdir)
            system(cmd)
            if cfg.is_verbose():
                write_kmsg(cmd);
            # Record st_dev of merge dir and pure upper file
            ctx.note_upper_fs(upper_mntroot, testdir, union_mntroot + "/f")
        ctx.note_mid_layers(mid_layers)
        ctx.note_upper_layer(upperdir)
