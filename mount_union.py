from tool_box import *

def mount_union(ctx):
    cfg = ctx.config()
    union_mntroot = cfg.union_mntroot()
    testdir = cfg.testdir()
    if cfg.testing_none():
        lower_mntroot = cfg.lower_mntroot()
        system("mount -o bind " + lower_mntroot + " " + union_mntroot)
        ctx.note_upper_fs(lower_mntroot, testdir, testdir)

    else:
        lower_mntroot = cfg.lower_mntroot()
        upper_mntroot = cfg.upper_mntroot()
        snapshot_mntroot = cfg.snapshot_mntroot()
        if cfg.should_mount_upper():
            system("mount " + upper_mntroot + " 2>/dev/null"
                    " || mount -t tmpfs upper_layer " + upper_mntroot)
        layer_mntroot = upper_mntroot + "/" + ctx.curr_layer()
        upperdir = layer_mntroot + "/u"
        workdir = layer_mntroot + "/w"
        nested_mntroot = upper_mntroot + "/n"
        nested_upper = upper_mntroot + "/u"
        nested_work = upper_mntroot + "/w"
        try:
            os.mkdir(layer_mntroot)
            if cfg.is_nested():
                os.mkdir(nested_mntroot)
        except OSError:
            system("rm -rf " + upper_mntroot + "/*")
            os.mkdir(layer_mntroot)
            if cfg.is_nested():
                os.mkdir(nested_mntroot)
        # Create unique fs for upper/0 if maxfs > 0
        if cfg.maxfs() > 0:
            system("mount -t tmpfs " + ctx.curr_layer() + "_layer " + layer_mntroot)
        os.mkdir(upperdir)
        os.mkdir(workdir)
        if not cfg.testing_snapshot():
            # Create pure upper file
            write_file(upperdir + "/f", "pure");
        if cfg.is_nested():
            os.mkdir(nested_upper)
            os.mkdir(nested_work)

        mntopt = " -orw" + cfg.mntopts()
        if cfg.is_nested():
            nested_mntopt = mntopt
            if cfg.is_verify():
                nested_mntopt = mntopt + ",metacopy=off,nfs_export=on"
            system("mount -t " + cfg.fstype() + " nested_layer " + nested_mntroot + nested_mntopt + ",lowerdir=" + lower_mntroot + ",upperdir=" + nested_upper + ",workdir=" + nested_work)
            lower_mntroot = nested_mntroot
            ctx.note_lower_fs(lower_mntroot)

        if cfg.testing_snapshot():
            curr_snapshot = snapshot_mntroot + "/" + ctx.curr_layer()
            try:
                os.mkdir(curr_snapshot)
            except OSError:
                pass

            mntopt = " -oredirect_dir=origin"
            if ctx.max_layers() > 0 and not cfg.is_metacopy():
                mntopt += ",index=on,nfs_export=on"
            # This is the latest snapshot of lower_mntroot:
            system("mount -t overlay overlay " + curr_snapshot + mntopt +
                   ",lowerdir=" + lower_mntroot + ",upperdir=" + upperdir + ",workdir=" + workdir)
            # This is the snapshot mount where tests are run
            snapmntopt = " -onoatime"
            # --sn --remount implies start with nosnapshot setup until first recycle
            if ctx.layers_nr() >= 0:
                snapmntopt += ",snapshot=" + curr_snapshot
            if cfg.is_metacopy():
                # don't copy files to snapshot only directories
                snapmntopt = snapmntopt + ",metacopy=on"
            system("mount -t snapshot " + lower_mntroot + " " + union_mntroot + snapmntopt)
            # Remount latest snapshot readonly
            system("mount " + curr_snapshot + " -oremount,ro")
            ctx.note_upper_fs(lower_mntroot, testdir, testdir)
        else:
            system("mount -t " + cfg.fstype() + " " + cfg.fsname() + " " + union_mntroot + mntopt +
                   ",lowerdir=" + lower_mntroot + ",upperdir=" + upperdir + ",workdir=" + workdir)
            # Record st_dev of merge dir and pure upper file
            ctx.note_upper_fs(upper_mntroot, testdir, union_mntroot + "/f")
        ctx.note_lower_layer(lower_mntroot)
        ctx.note_upper_layer(upperdir)
